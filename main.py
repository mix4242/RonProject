import numpy as np
import csv
import time

def updateWij(RomeA, RomeB, RomeV, cars):
    for i in range(RomeV):
        RomeV[i] = Rome


def RomeSimulate(RomeA):
    #find optimal route for each node to node dest
    #move 70% caars accordingly, rest stay <- calc 0.7 of num. floor. do cars-num, add num to optimal node
    #calc 60% of cars at node 52, floor. node 52 - num.
    #update wij
    updateWij(RomeA, RomeB, RomeV, cars)
    print RomeA
    


    return

if __name__ == "__main__":
    RomeA = np.empty(0,dtype=int)
    RomeB = np.empty(0,dtype=int)
    RomeV = np.empty(0,dtype=float)
    with open('RomeEdges','r') as file:
        AAA = csv.reader(file)
        for row in AAA:
            RomeA = np.concatenate((RomeA,[int(row[0])]))
            RomeB = np.concatenate((RomeB,[int(row[1])]))
            RomeV = np.concatenate((RomeV,[float(row[2])]))
    file.close()

    injectionPoint = 12 # St. Peter's Square
    destination = 51 # Coliseum
    cars = np.zeros(shape=58)



    for i in range(200):
        if i < 180:
            cars[injectionPoint] += 20
        RomeSimulate(RomeA, RomeB, RomeV, cars)