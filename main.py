import numpy as np
import csv
import math
import random

from Dijkstra import Dijkst

XI = 0.01

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
        
def RomeSimulate(RomeA, RomeB, wei, weiZeroth, cars):
    #find optimal route for each node to node dest
    nextNode = np.zeros(shape=58)
    for i in range(len(nextNode)):
        if i == 51:
            continue
        nextNode[i] = Dijkst(i,51,wei)[1]
    #move 70% caars accordingly, rest stay <- calc 0.7 of num. floor. do cars-num, add num to optimal node
    #print "et", nextNode[40]
    copyCars = np.copy(cars)
    for i in range(len(nextNode)):
        if i == 51:
            continue
        carsAtNode = copyCars[i]
        if carsAtNode == 1:
            if random.uniform(0.0, 1.0) <= 0.7:
                moving = 1
            else:
                moving = 0
        else:
            moving = int(math.floor(carsAtNode * 0.7))            
        cars[i] -= moving
        cars[int(nextNode[i])] += moving
    #calc 60% of cars at node 52, floor. node 52 - num.
    carsAt51 = cars[51]
    if carsAt51 == 1:
        if random.uniform(0.0, 1.0) <= 0.4:
            leave = 1
        else:
            leave = 0
    else:
        leave = carsAt51 - math.floor(0.6 * carsAt51)            
    cars[51] -= leave
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
        RomeSimulate(RomeA, RomeB, wei, weiZeroth, cars)
        count = 0
        nodes = []
        for j in range(len(cars)):
            if cars[j] != 0:
                count += 1
                nodes.append(j)
        print "nodes in use", count, nodes
        printCars(cars)
        print wei
