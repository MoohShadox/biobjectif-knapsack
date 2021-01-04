import numpy as np
import matplotlib.pyplot as plt
import time
from utils.pareto_optimal import pareto_front_sorted, pareto_optimal_MO, pareto_optimal_ameliore, pareto_optimal_naif, tirer

plot_points = lambda v,c:plt.scatter(v[:,0],v[:,1],c=c)

def plot_front(points, front):
    plt.xlabel("1er Objectif")
    plt.ylabel("2eme Objectif")
    plt.scatter(points[:,0],points[:,1],c="blue",label = "Dominés")
    plt.scatter(front[:,0],front[:,1],c="red", label="Efficaces")
    plt.legend()

def stress_test_mean(func,lower_born= 250, upper_born=2500, step = 250, loc=1000):
    logs = {
        "size":[],
        "time":[]
    }
    for nb_points in range(lower_born, upper_born, step):
        v = tirer(loc,nb_points)
        local_mean = []
        for i in range(50):
            t = time.time_ns()
            func(v)
            t = t - time.time_ns()
            local_mean.append(t)
        local_mean = np.array(local_mean).mean()
        logs["size"].append(nb_points)
        logs["time"].append(local_mean)
    return logs

def stress_test_conf(func,lower_born= 250, upper_born=2500, step = 250, loc=1000, nb_trys = 50):
    logs = {
        "size":[],
        "time":[],
        "name":[]
    }
    for nb_points in range(lower_born, upper_born+step, step):
        v = tirer(loc,nb_points)
        for i in range(nb_trys):
            t = time.time_ns()
            func(v)
            t =  time.time_ns() - t
            logs["size"].append(nb_points)
            logs["time"].append(t)
            logs["name"].append(func.__name__)
    return logs


