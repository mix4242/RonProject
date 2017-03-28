#Ronak Shah

import numpy as np
import sys

INFWEIGHT = 100000

def createWij(dependencies, durations):
    ## Create a weight matrix, I have generalised it for any network, 
    ## taking dependencies and job duration as the variables.
    num_jobs = len(durations)

    ## Initialize wei with constant 'infinite' value
    wij = np.full((2*num_jobs + 2, 2*num_jobs + 2), INFWEIGHT)

    ## Connect Virtual Start Node(index 0) to start node of every job
    ## and similarily connect the Virtual End Node(index 2*num_jobs+1) to
    ## end node of every job. Furthermore we include job durations, from
    ## the durations array, where index i is the duration of job i.
    for i in range(num_jobs):
        wij[0, 2*i + 1] = 0
        wij[2*i + 2, 2*num_jobs + 1] = 0
        wij[2*i + 1, 2*i + 2] = -durations[i]

    ## Set up job dependencies. Dependencies array is made of tuples.
    ## First of which is a job number and second is a first-job dependent.
    for k in range(len(dependencies)):
        wij[2 * dependencies[k, 0] + 2, 2 * dependencies[k, 1] + 1] = 0

    return wij

def amendWei(weights, l_path):
    weights_copy = np.copy(weights)
    m = len(weights_copy)
    evens = [x for x in l_path if x % 2 == 0]
    for i in evens:
        if (np.count_nonzero(weights_copy[i, :]) == m - 1) and (np.count_nonzero(weights_copy[:, i-1]) >= m - 2):
            weights_copy[i, m-1] = INFWEIGHT
            j = l_path.index(i)
            if j >= 2:
                a = l_path[j-2]
                b = l_path[j-1]
                weights_copy[a, b] = INFWEIGHT
        if np.count_nonzero(weights_copy[i, :]) == m - 1:
            j = l_path.index(i)
            if j >= 2:
                a = l_path[j-2]
                b = l_path[j-1]
                weights_copy[a, b] = INFWEIGHT
    return weights_copy

def BellmanFord(ist, isp, wei):
    #  ist:    index of starting node
    #  isp:    index of stopping node
    #  wei:    adjacency matrix (V x V)
    #  shpath: shortest path

    V = wei.shape[1]

    # step 1: initialization
    Inf = sys.maxint
    d = np.ones(V, float) * np.inf
    p = np.zeros(V, int) * Inf
    d[ist] = 0

    # step 2: iterative relaxation
    for i in range(0, V-1):
        for u in range(0, V):
            for v in range(0, V):
                w = wei[u, v]
                if w != INFWEIGHT:
                    if d[u]+w < d[v]:
                        d[v] = d[u] + w
                        p[v] = u

    # step 3: check for negative-weight cycles
    for u in range(0, V):
        for v in range(0, V):
            w = wei[u, v]
            if w != INFWEIGHT:
                if d[u]+w < d[v]:
                    print('graph contains a negative-weight cycle')

    # step 4: determine the shortest path
    shpath = [isp]
    while p[isp] != ist:
        shpath.append(p[isp])
        isp = p[isp]
    shpath.append(ist)

    return shpath[::-1]

if __name__ == '__main__':
    #indices of starting and stopping node respectively
    ist = 0
    isp = 27

    #set input variables for createWei
    dependencies = np.array([[0, 1], [0, 7], [0, 10], [1, 4], [1, 12], [2, 3], [5, 7], [6, 5], [6, 9], [9, 11], [10, 12]])
    duration = np.array((41, 51, 50, 36, 38, 45, 21, 32, 32, 49, 30, 19, 26))

    #create weight matrix
    wei = createWij(dependencies, duration)

    #initialise array of longest paths
    lpath_full = []

    #use modified BellamanFord to generate longest path
    lpath_full.append(BellmanFord(ist, isp, wei))

    for i in range(50):
        wei_new = amendWei(wei, lpath_full[i])
        lpath_full.append(BellmanFord(ist, isp, wei_new))
        wei = np.copy(wei_new)
        if lpath_full[i+1] == [0, 27]:
            break
    
    del lpath_full[len(lpath_full)-1]
    print(lpath_full)

    for i in range(len(lpath_full)):
        del lpath_full[i][0]
        del lpath_full[i][len(lpath_full[i])-1]
        for j in range(0, len(lpath_full[i]), 2):
            x = lpath_full[i][j]
            lpath_full[i][j] = (x-1) / 2
            lpath_full[i][j+1] = -1
        lpath_full[i] = [item for item in lpath_full[i] if item != -1]
    print(lpath_full)

