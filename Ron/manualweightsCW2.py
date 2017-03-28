import numpy as np
#build a weight matrix based on information given
#the weight matrix is (N*2 + 2)*(N*2 + 2) where N is the number of jobs
#we add 2 for the the virtual start and the virtual end nodes
#start with an array of infinity
wei = np.full((28,28), -1 * float('inf'))
#the virtual start node, index 0 is connected to all jobs' start node
#the finish node for all jobs is connected to the virtual finish node
for i in range(13):
    wei[0, 2*i+1] = 0
    wei[2*i+2, 27] = 0
#we now want to include information given in table 1.1
#start by setting each job start to each job finish with the job duration
#begin by initialising an array of durations 
durations = np.array((41,51,50,36,38,45,21,32,32,49,30,19,26))
#now loop over the weights matrix to include these values
for j in range(13):
    wei[2*j+1, 2*j+2] = durations[j]
#finally, account for job dependencies
#connect the end of job 0 to the start of jobs 1, 7 and 10
wei[2, 3] = 0
wei[2, 15] = 0
wei[2, 21] = 0
#connect the end of job 2 to the start of job 3
wei[6, 7] = 0
#connect the end of job 6 to the start of jobs 5 and 9
wei[14, 11] = 0
wei[14, 19] = 0
#connect the end of job 1 to the start of jobs 4 and 12
wei[4, 9] = 0
wei[4, 15] = 0
#connect the end of job 10 to the start of job 12
wei[22, 25] = 0
#connect the end of job 5 to the start of job 7
wei[12, 15] = 0
#connect the end of job 9 to the start of job 11
wei[20, 23] = 0
#this completes our weight matrix
#negate the weight matrix in order to do a longest path test
wei = -1 * wei