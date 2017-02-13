import numpy as np
import csv
import math

from Dijkstra import Dijkst

XI = 0.01

def calcWei(RA,RB,RV):
    n    = len(RA) / 2
    wei = np.zeros((n,n),dtype=float)
    for i in range(len(RA)):
        wei[RA[i]-1,RB[i]-1] = RV[i]
    return wei

def updateWij(RomeA, RomeB, Wij, WijOrig, cars):
    for i in range(len(Wij)):
        Wij[i] = WijOrig[i] + XI * ((cars[RomeA[i]-1] + cars[RomeB[i]-1])/2)

def RomeSimulate(RomeA, RomeB, Wij, WijOrig, cars):
    #find optimal route for each node to node dest
    dWij = calcWei(RomeA, RomeB, Wij)
    nextNode = Dijkst(12,52,dWij)
    print dWij
    #move 70% caars accordingly, rest stay <- calc 0.7 of num. floor. do cars-num, add num to optimal node
    copyCars = np.copy(cars)
    for i in range(len(nextNode)):
        moving = math.floor(cars[i] * 0.7)
        copyCars[i] -= moving
        copyCars[Dijkst(i+1,52,dWij)[0]] += moving
        #if moving != 0:
        #print moving
    cars = copyCars
    #calc 60% of cars at node 52, floor. node 52 - num.
    cars[51] -= math.floor(0.4 * cars[51])
    #update wij
    updateWij(RomeA, RomeB, Wij, WijOrig, cars)
    return

if __name__ == "__main__":
    RomeA = np.empty(0,dtype=int)
    RomeB = np.empty(0,dtype=int)
    Wij = np.empty(0,dtype=float)
    WijOrig = np.empty(0,dtype=float)
    with open('RomeEdges','r') as file:
        AAA = csv.reader(file)
        for row in AAA:
            RomeA = np.concatenate((RomeA,[int(row[0])]))
            RomeB = np.concatenate((RomeB,[int(row[1])]))
            Wij = np.concatenate((Wij,[float(row[2])]))
            WijOrig = np.concatenate((WijOrig,[float(row[2])]))
    file.close()

    injectionPoint = 12 # St. Peter's Square
    destination = 51 # Coliseum
    cars = np.zeros(shape=58)
    print "Simulating Rome #Roger"
    for i in range(200):
        if i < 180:
            cars[injectionPoint] += 20
        RomeSimulate(RomeA, RomeB, Wij, WijOrig, cars)