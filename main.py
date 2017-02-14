import numpy as np
import csv
import math

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

def calcWei(RA,RB,RV):
    n    = 58
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
    nextNode = np.zeros(shape=58)
    for i in range(len(nextNode)):
        if i == 51:
            continue
        nextNode[i] = Dijkst(i,51,dWij)[1]
    #move 70% caars accordingly, rest stay <- calc 0.7 of num. floor. do cars-num, add num to optimal node
    #print "Next Node", nextNode[12]
    copyCars = np.copy(cars)
    for i in range(len(nextNode)):
        moving = int(math.floor(copyCars[i] * 0.7))
        #if moving != 0:
        #print moving
        cars[i] -= moving
        cars[int(nextNode[i])] += moving
    #calc 60% of cars at node 52, floor. node 52 - num.
    cars[51] -= int(math.floor(0.4 * cars[51]))
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
    print "Simulating Rome #Roger\nInitial state:"
    printCars(cars)
    for i in range(200):
        if i < 180:
            cars[injectionPoint] += 20
        print "#############################################"
        print "Simulating iteration: ", i+1
        RomeSimulate(RomeA, RomeB, Wij, WijOrig, cars)
        printCars(cars)