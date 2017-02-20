import numpy as np
import csv
import math
import random

from Dijkstra import Dijkst

XI = 0.10
NUMNODES = 58
RANGEEX51 = range(NUMNODES)
RANGEEX51.remove(51)

def printNode(node):
    return str(node)

def printCar(car):
    return str(car)
    
def printCars(cars):
    columnCars = len(cars)-2
    for i in range(0, columnCars, 4):
        print "%s: %s, %s: %s, %s: %s, %s: %s," % (printNode(i+1),printCar(cars[i]),printNode(i+2),printCar(cars[i+1]),printNode(i+3),printCar(cars[i+2]),printNode(i+4),printCar(cars[i+3]))
    print "%s: %s, %s: %s" % (printNode(columnCars+1),printCar(cars[columnCars]),printNode(columnCars+2),printCar(cars[columnCars+1]))

def fillWei(RA,RB,RV):
    n = NUMNODES
    wei = np.zeros((n,n),dtype=float)
    for i in range(len(RA)):
        wei[RA[i]-1,RB[i]-1] = RV[i]
    return wei

def updateWij(RomeA, RomeB, wei, weiZeroth, cars):
    for n in range(len(RomeA)):
        i = RomeA[n]-1
        j = RomeB[n]-1
        wei[i,j] = weiZeroth[i,j] + (XI * ((cars[i] + cars[j]) / 2 ) )

nextNode = np.zeros(shape=58)
def RomeSimulate(RomeA, RomeB, wei, weiZeroth, cars, nodeLoad):
    global nextNode
    for i in range(len(nextNode)):
        if i == 51:
            continue
        nextNode[i] = int(Dijkst(i,51,wei)[1])

    carsAt51 = cars[51]
    nodeLoad[51] = max(nodeLoad[51], carsAt51)
    cars[51] = math.floor(0.6 * carsAt51)

    copyCars = np.copy(cars)
    for i in RANGEEX51:
        carsAtNode = copyCars[i]
        nodeLoad[i] = max(nodeLoad[i], carsAtNode)
        oldCars = cars[i]
        carsLeft = math.floor(oldCars - 0.7 * carsAtNode)
        cars[i] = carsLeft
        carsMoved = oldCars - carsLeft
        cars[int(nextNode[i])] += carsMoved
    
    updateWij(RomeA, RomeB, wei, weiZeroth, cars)
    return

def blockNode30(weiZeroth):
    weiZeroth[29, 25] = 9999
    weiZeroth[29, 34] = 9999
    weiZeroth[29, 42] = 9999
    weiZeroth[29, 44] = 9999
    weiZeroth[29, 20] = 9999

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

    injectionPoint = 12
    destination = 51
    cars = np.zeros(shape=58)
    nodeLoad = np.zeros(shape=58)
    wei = fillWei(RomeA, RomeB, RomeV)
    weiZeroth = np.copy(wei)

    #blockNode30(weiZeroth)

    print "Simulating Rome #Roger\nInitial state:"
    printCars(cars)
    for i in range(200):
        if i < 180:
            cars[injectionPoint] += 20
        print "#############################################"
        print "Simulating iteration: ", i+1
        RomeSimulate(RomeA, RomeB, wei, weiZeroth, cars, nodeLoad)
        #count = 0
        #nodes = []
        #for j in range(len(cars)):
        #    if cars[j] != 0:
        #        count += 1
        #        nodes.append(j)
        #print "nodes in use", count, nodes
        printCars(cars)
    printCars(nodeLoad)
