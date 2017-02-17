import numpy as np
import csv
import math
import random

from Dijkstra import Dijkst

XI = 0.01
RANGEEX51 = range(58)
RANGEEX51.remove(51)

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def printNode(node):
    return bcolors.OKGREEN + str(node) + bcolors.ENDC

def printCar(car):
    return bcolors.BOLD + bcolors.FAIL + str(car) + bcolors.ENDC

def printCars(cars):
    for i in range(0, len(cars)-2, 4):
        print "%s: %s, %s: %s, %s: %s, %s: %s," % (printNode(i+1),printCar(cars[i]),printNode(i+2),printCar(cars[i+1]),printNode(i+3),printCar(cars[i+2]),printNode(i+4),printCar(cars[i+3]))
    print "%s: %s, %s: %s" % (printNode(57),printCar(cars[56]),printNode(58),printCar(cars[57]))

def fillWei(RA,RB,RV):
    n = 58
    wei = np.zeros((n,n),dtype=float)
    for i in range(len(RA)):
        wei[RA[i]-1,RB[i]-1] = RV[i]
    return wei

def updateWij(RomeA, RomeB, wei, weiZeroth, cars):
    for n in range(len(RomeA)):
        i = RomeA[n]-1
        j = RomeB[n]-1
        wei[i,j] = weiZeroth[i,j] + (XI * ((cars[i] + cars[j]) / 2 ) )
        
def RomeSimulate(RomeA, RomeB, wei, weiZeroth, cars, nodeLoad):
    #find optimal route for each node to node dest
    nextNode = np.zeros(shape=58)
    for i in range(len(nextNode)):
        if i == 51:
            continue
        nextNode[i] = Dijkst(i,51,wei)[1]
    #move 70% caars accordingly, rest stay <- calc 0.7 of num. floor. do cars-num, add num to optimal node
    #print "et", nextNode[40]
    copyCars = np.copy(cars)
    for i in RANGEEX51:
        carsAtNode = copyCars[i]
        nodeLoad[i] = max(nodeLoad[i], carsAtNode)
        oldCars = cars[i]
        cars[i] = math.floor(oldCars - 0.7 * carsAtNode)
        carsMoved = oldCars - cars[i]
        cars[int(nextNode[i])] += carsMoved

    #Node 52. 60% of cars stay.
    cars[51] = math.floor(0.6 * cars[51])
    nodeLoad[51] = max(nodeLoad[51], cars[51])
    #update wij
    oldwij = np.copy(wei)
    updateWij(RomeA, RomeB, wei, weiZeroth, cars)
    from functools import reduce
    product = (oldwij == wei).all()
    print "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa", product 
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
    nodeLoad = np.zeros(shape=58)
    wei = fillWei(RomeA, RomeB, RomeV)
    weiZeroth = np.copy(wei)
    print "Simulating Rome #Roger\nInitial state:"
    printCars(cars)
    #print wei
    for i in range(200):
        if i < 180:
            cars[injectionPoint] += 20
        print "#############################################"
        print "Simulating iteration: ", i+1
        RomeSimulate(RomeA, RomeB, wei, weiZeroth, cars, nodeLoad)
        count = 0
        nodes = []
        for j in range(len(cars)):
            if cars[j] != 0:
                count += 1
                nodes.append(j)
        print "nodes in use", count, nodes
        printCars(cars)
        print wei
    printCars(nodeLoad)
