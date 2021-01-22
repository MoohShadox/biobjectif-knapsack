import copy
import numpy as np
from itertools import combinations

get_random_cost = lambda  n: np.abs(np.random.normal(0,100,(2,n)).astype(int))

def test_dynamic_prog(n,k,c):

    get_random_bag = lambda  : np.random.randint(0,2,(n,1))
    get_cost = lambda x,c : (c@x).T.flatten()

    def get_cost_item_ids(xs,c):
        v= np.zeros((n,1))
        for x in xs:
            v[x-1] = 1
        return (v,c@v.reshape((-1)))

    def get_cost_item_msq(v,c):
        return c@v.reshape((-1))

    def print_table(prog_table):
        for i in range(k+1):
            for j in range(n+1):
                print(f"[{i}, {j}] : ",prog_table[i][j])

    def pf(costs):
        or_costs = costs
        is_efficient = np.arange(costs.shape[0])
        n_points = costs.shape[0]
        next_point_index = 0
        while next_point_index<len(costs):
            nondominated_point_mask = np.any(costs<costs[next_point_index], axis=1)
            nondominated_point_mask[next_point_index] = True
            is_efficient = is_efficient[nondominated_point_mask]
            costs = costs[nondominated_point_mask]
            next_point_index = np.sum(nondominated_point_mask[:next_point_index])+1

        is_efficient_mask = np.zeros(n_points, dtype = bool)
        is_efficient_mask[is_efficient] = True

        return is_efficient+1,is_efficient_mask,  or_costs[is_efficient_mask, :]

    class Bag():

        def __init__(self,ids=[]):
            self.cost = (0,0)
            self.ids = []
            self.msq = np.zeros(n)
            self.set_ids(ids)

        def set_ids(self, ids):
            ids = sorted(ids)
            v,m = get_cost_item_ids(ids,c)
            self.cost = m
            self.msq = v
            self.ids = ids

        def add_item(self,id):
            L = list(self.ids)
            if not id in self.ids:
                L.append(id)
            self.ids = np.array(L)
            self.set_ids(self.ids)

        def __str__(self):
            return f"{self.ids}"

        def set_msq(self,msq):
            self.ids = np.where(msq == 1)[0] + 1
            self.set_ids(self.ids)

        def __add__(self,b2):
            s = Bag([])
            id_u = list(self.ids) + list(b2.ids)
            id_u = set(id_u)
            id_u = list(id_u)
            s.set_ids(id_u)
            return s

        def __eq__(self, other):
            return sorted(self.ids) == sorted(other.ids)

    class Cell():
        def __init__(self):
            self.bags = []
            self.costs = []

        def add_bag(self, bag):
            bg = copy.deepcopy(bag)
            self.bags.append(bg)
            L = list(self.costs)
            L.append(bg.cost)
            self.costs = np.array(L)

        def set_bag(self, bag):
            self.bags = []
            self.bags.append(bag)
            L = []
            L.append(bag.cost)
            self.costs = np.array(L)

        def __copy__(self):
            c = Cell()
            c.costs = np.copy(self.costs)
            c.bags = list(self.bags)


        def apply_pf(self):
            costs = np.array(self.costs)
            ids,msq ,c  = (pf(costs))
            self.bags = np.array(self.bags)[ids-1]
            self.costs = c

        def add_item_to_all(self,index):
           for b in self.bags:
               b.add_item(index)

        def __getitem__(self,key):
            return self.bags[key]


        def __add__(self,cell):
           C = Cell()
           for b in cell.bags:
               C.add_bag(b)
           for b in self.bags:
               C.add_bag(b)
           return C

        def __eq__(self, other):
            if(len(self.bags) != len(other.bags)):
                return False

            for b1 in self.bags:
                if(b1 not in other.bags):
                    return False
            return True


        def __str__(self):
            return  "\t".join([str(b) for b in self.bags])

    def solve_exhaustif():

        i = combinations(np.arange(1,n+1),r = k)
        C = Cell()
        for j in i:
            b = Bag()
            b.set_ids(list(j))
            C.add_bag(b)
        #print(C)
        C.apply_pf()
        #print(C)
        return C

    def solve_dynamic_programming():
        prog_table = [[ (Cell()) for x in range(n + 1)] for x in range(k + 1)]
        prog_table = np.array(prog_table)

        obj = np.arange(1,n+1)
        for i in range(1,n+1):
            bag = (pf(c.T[obj[:i] - 1])[0])
            #print(i,bag)
            for b in bag:
                B = Bag([b])
                prog_table[1][i].add_bag(B)

        for i in range(1,k+1):
            b= Bag(obj[:i])
            #print(b)
            prog_table[i][i].set_bag(b)

        for i in range(2,k+1):
            for j in range(3,n+1):
                if(j < i):
                    continue
                #print()
                #print(f"In Cell [{i},{j}]")
                c1 = prog_table[i-1][j-1]
                c2 = prog_table[i][j-1]
                #print(f"[{i-1},{j-1}] : ", c1)
                #print(f"[{i},{j-1}] : ", c2)
                c3 = c1
                c3.add_item_to_all(j)
                c4 = c2 + c3
                #print("The contenant before pf is : ",c4)
                c4.apply_pf()
                #print(f"so the in  [{i},{j}] is : ",c4)
                prog_table[i][j] = c4
        return prog_table[k][n]
    return solve_dynamic_programming, solve_exhaustif
