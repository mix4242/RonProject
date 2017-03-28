#Ronak Shah

import numpy as np
import sys
import plotly
import plotly.plotly as py
import plotly.figure_factory as ff

INFWEIGHT = 999

def ModBellmanFord(ist, isp, wij):
    #  ist:    index of starting node
    #  isp:    index of stopping node
    #  wei:    adjacency matrix (V x V)
    #  shpath: shortest path

    V = wij.shape[1]

    # step 1: initialization
    Inf = sys.maxint
    d = np.ones(V, float) * np.inf
    p = np.zeros(V, int) * Inf
    d[ist] = 0

    # step 2: iterative relaxation
    for i in range(0, V-1):
        for u in range(0, V):
            for v in range(0, V):
                w = wij[u, v]
                if w != INFWEIGHT:
                    if d[u]+w < d[v]:
                        d[v] = d[u] + w
                        p[v] = u

    # step 3: check for negative-weight cycles
    for u in range(0, V):
        for v in range(0, V):
            w = wij[u, v]
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

## Takes time in minutes and returns in analogue form, after 9am
def toHrsMins(mins):
    minutes = mins % 60
    hours = mins / 60
    return str(hours+9) + ":" + ("0" if minutes < 10 else "") + str(minutes) + ":00"

## Prints the Gantt graph as a HTML5 document
def printGantt(jobs):
    df = []
    for i in range(len(jobs)):
        job = dict(Task="Job " + str(i), Start='2009-01-01 ' + toHrsMins(jobs[i][0]) , Finish='2009-01-01 ' + toHrsMins(jobs[i][1]))
        df.append(job)

    fig = ff.create_gantt(df)
    plotly.offline.plot(fig, filename='gantt-simple-gantt-chart.html')

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

def updateWij(wij, longest_path):
    weights_copy = np.copy(wij)
    m = len(weights_copy)

    ## Get all the End Nodes of the longest path jobs
    evens = [x for x in longest_path if x % 2 == 0]
    for i in evens:
        if (np.count_nonzero(weights_copy[i, :]) == m - 1) and (np.count_nonzero(weights_copy[:, i-1]) >= m - 2):
            weights_copy[i, m-1] = INFWEIGHT
            ## Find first occurance of End Node
            j = longest_path.index(i)
            if j >= 2:
                a = longest_path[j-2]
                b = longest_path[j-1]
                weights_copy[a, b] = INFWEIGHT
        if np.count_nonzero(weights_copy[i, :]) == m - 1:
            ## Find first occurance of End Node
            j = longest_path.index(i)
            if j >= 2:
                a = longest_path[j-2]
                b = longest_path[j-1]
                weights_copy[a, b] = INFWEIGHT
    return weights_copy

if __name__ == '__main__':
    ## Virtual Start and End nodes
    VSN = 0
    VEN = 27

    ## Initialize longest path array
    longest_path = []

    ## Set up dependencies and job durations as per question
    dependencies = np.array([[0, 1], [0, 7], [0, 10], [1, 4], [1, 12], [2, 3], [5, 7], [6, 5], [6, 9], [9, 11], [10, 12]])
    duration = np.array((41, 51, 50, 36, 38, 45, 21, 32, 32, 49, 30, 19, 26))

    wij = createWij(dependencies, duration)

    ## Find the first longest path using our modified BellamanFord function
    longest_path.append(ModBellmanFord(VSN, VEN, wij))

    while True:
        last_path = len(longest_path)-1
        wij_new = updateWij(wij, longest_path[last_path])
        next_path = ModBellmanFord(VSN, VEN, wij_new)
        if next_path == [0,27]:
            ## If the longest path doesnt include any 'real' nodes, break out
            break
        longest_path.append(next_path)
        wij = np.copy(wij_new)
    
    print(longest_path)

    ## Logic for turning longest paths into list of jobs
    for i in range(len(longest_path)):
        ## Remove the Virtual Start/End Nodes from the list
        del longest_path[i][0]
        del longest_path[i][len(longest_path[i])-1]

        ## Take the first index and turn it into job number, set second to -1 to be deleted later
        for j in range(0, len(longest_path[i]), 2):
            x = longest_path[i][j]
            longest_path[i][j] = (x-1) / 2
            longest_path[i][j+1] = -1

        ## Delete all -1's
        longest_path[i] = [item for item in longest_path[i] if item != -1]
    
    #print(longest_path)
    longest_path.reverse()

    ## Initialize new job times variable, set all start/end times to 0
    job_times = []
    for i in range(len(duration)):
        job_times.append([0, 0])

    for i in range(len(longest_path)):
        ## The collective run time is set to 0 for every job path
        run_time = 0
        for j in range(len(longest_path[i])):
            job = longest_path[i][j]
            job_times[job][0] = run_time
            run_time += duration[job]
            job_times[job][1] = run_time
    
    ## Print all the nodes' start and end times
    print ("Node: Start - End")
    for i in range(len(job_times)):
        print ("%d: %d - %d" % (i, job_times[i][0], job_times[i][1]))
    
    ## Create Gantt graph
    printGantt(job_times)
