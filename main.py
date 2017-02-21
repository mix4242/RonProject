import numpy as np
import csv
import math

from Dijkstra import Dijkst, calcWei

XI = 0.01
NUMNODES = 58
START = 12 # St. Peter's Square
END = 51 # Coliseum
RANGEEXEND = range(NUMNODES)
RANGEEXEND.remove(END) #Range of nodes, without the END node

class bcolors:
    #Define special character sequences as colors to be used.
    #Work only on Unix
    OKGREEN = '\033[92m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

def printNode(node):
    #Wraps node number in color
    return bcolors.OKGREEN + str(node) + bcolors.ENDC

def printCar(car):
    #Wraps car number in color
    return bcolors.BOLD + bcolors.FAIL + str(car) + bcolors.ENDC

def printCars(cars):
    #Prints out the cars at each node in a concise, shorter format of 4 colums
    columnCars = NUMNODES-2
    for i in range(0, columnCars, 4):
        print "%s: %s, %s: %s, %s: %s, %s: %s," % (printNode(i+1),printCar(cars[i]),printNode(i+2),printCar(cars[i+1]),printNode(i+3),printCar(cars[i+2]),printNode(i+4),printCar(cars[i+3]))
    print "%s: %s, %s: %s" % (printNode(columnCars+1),printCar(cars[columnCars]),printNode(columnCars+2),printCar(cars[columnCars+1]))

def updateWij(RomeA, RomeB, wij, wijZeroth, cars):
    #Updates the weights according to the given formula
    for n in range(len(RomeA)):
        i = RomeA[n]-1
        j = RomeB[n]-1
        wij[i,j] = wijZeroth[i,j] + (XI * ((cars[i] + cars[j]) / 2))

def RomeSimulate(RomeA, RomeB, wij, wijZeroth, cars, nodeLoad, nextNode):
    #find optimal route for each node to node END
    for i in RANGEEXEND:
        #The 1st elem of the returned array is next node to travel to
        nextNode[i] = int(Dijkst(i,END,wij)[1])

    #Node END. 60% of cars stay.
    carsAtEND = cars[END]
    nodeLoad[END] = max(nodeLoad[END], carsAtEND)
    cars[END] = round(0.6 * carsAtEND)

    #Move the cars at all other nodes except END
    copyCars = np.copy(cars)
    for i in RANGEEXEND:
        carsAtNode = copyCars[i]
        nodeLoad[i] = max(nodeLoad[i], carsAtNode)
        oldCars = cars[i]
        carsLeft = round(oldCars - 0.7 * carsAtNode)
        cars[i] = carsLeft
        carsMoved = oldCars - carsLeft
        cars[int(nextNode[i])] += carsMoved
    
    #update wij
    updateWij(RomeA, RomeB, wij, wijZeroth, cars)
    return

#This method sets the weights of outgoing edges of node 30 to 9999
#This means node will never be used
def blockNode30(wijZeroth):
    wijZeroth[29, 25] = 9999
    wijZeroth[29, 34] = 9999
    wijZeroth[29, 42] = 9999
    wijZeroth[29, 44] = 9999
    wijZeroth[29, 20] = 9999

if __name__ == "__main__":
    #Get the x and y values of Romes' vertices
    RomeX = np.empty(0,dtype=float)
    RomeY = np.empty(0,dtype=float)
    with open('RomeVertices','r') as file:
        AAA = csv.reader(file)
        for row in AAA:
            RomeX = np.concatenate((RomeX,[float(row[1])]))
            RomeY = np.concatenate((RomeY,[float(row[2])]))
    file.close()

    #Get the edge values and initial weight values of Romes' edges
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

    #Initialize arrays
    cars = np.zeros(shape=NUMNODES)
    nodeLoad = np.zeros(shape=NUMNODES)
    nextNode = np.zeros(shape=NUMNODES)

    #Calculate initial weights of edges
    wij = calcWei(RomeX, RomeY, RomeA, RomeB, RomeV)
    wijZeroth = np.copy(wij)

    #blockNode30(wijZeroth)

    print "Simulating Rome\nInitial state:"
    printCars(cars)
    for i in range(200):
        if i < 180:
            cars[START] += 20
        print "#############################################"
        print "Simulating iteration: ", i+1
        RomeSimulate(RomeA, RomeB, wij, wijZeroth, cars, nodeLoad, nextNode)
        printCars(cars)
        
    print "Maximum Node Load:"
    #We can use same func for printing cars to print the load for each node
    printCars(nodeLoad)
