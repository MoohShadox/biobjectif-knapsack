import pareto_optimal
from inspect import getmembers, isfunction
from importlib import import_module
import unittest
from pareto_optimal import tirer ,lex_sort
from dynamic_prog import *
import numpy as np


class TestSum(unittest.TestCase):

    def test_every_pareto_alg(self):
        func_dict = {}
        for i,j in (getmembers(pareto_optimal, isfunction)):
            if(i.startswith("pareto")):
                my_function = getattr(__import__('pareto_optimal'), i)
                func_dict[my_function] = []

        v = tirer(1000,5).astype(int)

        for i in func_dict.keys():
            val = i(v)
            func_dict[i] = val


        for i,f1 in enumerate(func_dict.keys()):
            for j,f2 in enumerate(list(func_dict.keys())[i+1:]):
                print(f"Checking if {f1.__name__} and {f2.__name__} gave the same ")
                t = ((lex_sort(func_dict[f1]) == lex_sort(func_dict[f2])).all())
                self.assertEqual(t, True)
                print(u'\u2705')
    

    def test_prog_solving(self):
        for n in range(3,14):
            for k in range(1,n):
                c = get_random_cost(n)
                f,g = test_dynamic_prog(n,k,c)
                c1 = f()
                c2 = g()
                print(f"Testing for k = {k}, n = {n}")
                self.assertEqual(c1 == c2, True)
                print(u'\u2705')



if __name__ == '__main__':
    unittest.main()
    


