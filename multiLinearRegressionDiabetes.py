import random
import math

print("Hello world!")

# Class handles static data set and creates a list of theta objects corresponding to it
# This class is capable of performing a multiple linear regression
class ThetaNumerical:

    ################################################## Static Vars and Methods
    inputDataPoints = [[1, 2, 3, 4, 5, 6, 7]]
    outputDataPoints = [2, 4, 6, 8, 10, 12, 14]
    alpha = 0.01
    deltaJ = 0.01

    # Changes alpha
    def changeAlpha(newAlpha):
        ThetaNumerical.alpha = float(newAlpha)

    # This method takes a list of lists. The outer list corresponds to dimensionality and represents data points.
    # Each sub list represent a point value for a single dimension
    def changeDataPoints(newInputDataPoints, newOutputDataPoints):
        if len(newInputDataPoints[0]) < 2:
            raise Exception("Data entered is not of sufficient length. Please enter a list of lists.")
        
        for x in range(len(newInputDataPoints)):
            if len(newInputDataPoints[x]) != len(newInputDataPoints[0]):
                raise Exception("Lists must have the same number of values.")
        
        if len(newInputDataPoints[0]) != len(newOutputDataPoints):
            raise Exception("Input data and output data must have the same number of data points.")

        ThetaNumerical.inputDataPoints = newInputDataPoints
        ThetaNumerical.outputDataPoints = newOutputDataPoints

    # Changes deltaJ
    def changeDeltaJ(newDeltaJ):
        ThetaNumerical.deltaJ = float(newDeltaJ)

    ################################################## Object manipulation
    # Changes value of theta
    def changeValue(self, newValue):
        self.thetaValue = newValue

    # Returns label of theta (theta0, theta1, theta2, etc.)
    def getLabel(self):
        return self.label
    
    # Returns numerical value of theta
    def getValue(self):
        return self.thetaValue

    # Using the dimensionality of the input data, this method creates the proper amount of theta variables and assigns them a random value
    def initializeThetaNumerical():
        tempList = []
        for x in range(len(ThetaNumerical.inputDataPoints) + 1):
            tempList.append(ThetaNumerical(random.randrange(1, 5, 1), x))
        return tempList

    ################################################## Mathematical Operations
    # Calculates a J value based on theta values and input/output data
    def calcJ(thetaList):
        totalSum = 0
        
        # Loop through xi/yi
        for i in range(len(ThetaNumerical.outputDataPoints)):
            tempCalc = 0
            
            # Loop through thetas (left to right within summation)
            for theta in thetaList:
                if theta.getLabel() == 0: # for theta0
                    tempCalc += theta.getValue()
                else:
                    tempCalc += theta.getValue() * ThetaNumerical.inputDataPoints[theta.getLabel() - 1][i]
            
            tempCalc -= ThetaNumerical.outputDataPoints[i] # subtract yi
            tempCalc *= tempCalc # square
            totalSum += tempCalc
        
        return totalSum/(2 * len(ThetaNumerical.outputDataPoints))

    # This is the main method for the mathematics section, as it calls the other ones
    # This method performs a gradient descent using an input list of initialized theta values and the input/outputdatapoints
    def gradientDescent(thetaList):
        continueCalc = True
        oldJ = None
        
        # Loops until deltaJ specification
        while continueCalc:
            derivativeList = []
            
            # Take the partial derivative of each theta value
            for theta in thetaList:
                if theta.getLabel() == 0:
                    derivativeList.append(ThetaNumerical.thetaZeroDerivative(thetaList))
                else:
                    derivativeList.append(ThetaNumerical.thetaStandardDerivative(theta, thetaList))

            # Apply alpha and partial derivative to current theta
            thetaList = ThetaNumerical.updateThetaNumerical(thetaList, derivativeList)

            # Calculate and check j
            j = ThetaNumerical.calcJ(thetaList)
            if oldJ != None and abs(j - oldJ) < ThetaNumerical.deltaJ:
                continueCalc = False
            else:
                oldJ = j
        
        return thetaList

    # Takes a list of theta and calculates corresponding theoretical value with input data
    def runFunction(thetaList):
        
        predictedValues = []

        # Ensures that the the number of thetas is supported by the dataset
        if len(thetaList) != len(ThetaNumerical.inputDataPoints) + 1:
            raise Exception("Theta list is not of sufficient length. Please ensure the the number of theta entries is the same as the dimensionality of the input data")
        
        # Isolate theta0 and remove it from the main list
        thetaZero = thetaList[0]
        thetaList.pop(0)

        # Calculation for a given point
        for dataPoint in range(len(ThetaNumerical.inputDataPoints[0])):
            theoreticalValue = thetaZero.getValue()
            for dimension in range(len(ThetaNumerical.inputDataPoints)):
                theoreticalValue += ThetaNumerical.inputDataPoints[dimension][dataPoint] * (thetaList[dimension]).getValue()
            
            print("at data point " + str(dataPoint) + " the theoretical value is " + str(theoreticalValue))
            predictedValues.append(theoreticalValue)
        
        return predictedValues

    # Takes the partial derivative of entered theta value (any except for theta0)
    def thetaStandardDerivative(inputThetaNumerical, thetaList):
        totalSum = 0
        
        # Loop through xi/yi
        for i in range(len(ThetaNumerical.outputDataPoints)):
            tempCalc = 0
            
            # Loop through thetas (left to right within summation)
            for theta in thetaList:
                if theta.getLabel() == 0:
                    tempCalc += theta.getValue()
                else:
                    tempCalc += theta.getValue() * ThetaNumerical.inputDataPoints[theta.getLabel() - 1][i]

            tempCalc -= ThetaNumerical.outputDataPoints[i] # Subtract yi
            tempCalc *= ThetaNumerical.inputDataPoints[inputThetaNumerical.getLabel() - 1][i] # Multiply by xi before summation
            totalSum += tempCalc
        
        return totalSum/len(ThetaNumerical.outputDataPoints)

    # Takes the partial derivative of entered theta value (any except for theta0)
    # Same as the StandardDerivative method but without multiplying by xi before summation
    def thetaZeroDerivative(thetaList):
        totalSum = 0
        
        # Loop through xi/yi
        for i in range(len(ThetaNumerical.outputDataPoints)):
            
            # Loop through thetas (left to right within summation)
            for theta in thetaList:
                if theta.getLabel() == 0:
                    totalSum += theta.getValue()
                else:
                    totalSum += theta.getValue() * ThetaNumerical.inputDataPoints[theta.getLabel() - 1][i]

            totalSum -= ThetaNumerical.outputDataPoints[i] # subtract yi
        
        return (totalSum)/len(ThetaNumerical.outputDataPoints)

    # This method is most relevant with gradient descent, updating the list of theta objects with new calculated values
    # This is done following derivative calculation as to not mess up the derivative calculations for sequential theta values
    def updateThetaNumerical(thetaList, derivativeList):
        for i in range(len(thetaList)):
            thetaList[i].changeValue(thetaList[i].getValue() - (ThetaNumerical.alpha * derivativeList[i]))
        return thetaList

    ################################################## Class Methods
    def __init__(self, theta, label):
        self.thetaValue = float(theta)
        self.label = label

    def __str__(self):
        return "theta" + str(self.label) + " has a value of " + str(self.thetaValue)


def average(numbers):
    return (sum(numbers)/len(numbers))

# Set list of numbers between -1 and 1
def fixRange(numbers):
    tempList = []
    for x in numbers:
        tempList.append((2 * ((x - min(numbers))/(max(numbers)-min(numbers)))) - 1)
    return tempList

def max(numbers):
    temp = numbers [0]
    for x in numbers:
        if x > temp:
            temp = x
    return temp

def min(numbers):
    temp = numbers [0]
    for x in numbers:
        if x < temp:
            temp = x
    return temp

# For reading in CSV tables
def parseCSV(filePath):
    listOfLists = []
    with open(filePath, "r") as fileContent:
        
        # Read line by line
        for line in fileContent:
            line = line.strip()
            splitLine = line.split(",")
            
            # Breaks line into entries
            for value in range(len(splitLine)):
                
                # If block breaks columns into lists and places those lists into one big list
                if len(listOfLists) != len(splitLine):
                    if splitLine[value] != "":
                        listOfLists.append([splitLine[value]])
                    else:
                        listOfLists.append(["Unlabeled"])
                else:
                    listOfLists[value].append(float(splitLine[value]))
    
    return listOfLists

def rSquared(predictionList, actualList):
    if len(predictionList) != len(actualList):
            raise Exception("Prediction list and actual data list must be of the same length.")

    sumNum = 0
    sumDen = 0
    mean = average(actualList)
    
    for i in range(len(actualList)):
        sumNum += (actualList[i] - predictionList[i]) ** 2
        sumDen += (actualList[i] - mean) ** 2
    
    return (1 - (sumNum/sumDen))

def standardDeviation(numbers):
        totalSum = 0
        
        # Loop through summation
        for x in numbers:
            totalSum += (x - average(numbers)) ** 2
        
        totalSum = math.sqrt(totalSum/(len(numbers) - 1))
        return totalSum

def zScore(numbers):
    tempData = []
    for x in numbers:
        tempData.append((x - average(numbers))/standardDeviation(numbers))
    return tempData


# MAIN METHOD

# Read in CSV
filePath = "C:\\Users\\Jacob\\Desktop\\Wormhole\\Fall2024\\MachineLearning\\HW2\\diabetes_dataset.csv"
allData = parseCSV(filePath)

# Parse data and pretreat (from -1 to 1)
age = fixRange(allData[0][1:])
sex = fixRange(allData[1][1:])
bmi = fixRange(allData[2][1:])
bp = fixRange(allData[3][1:])
s1 = fixRange(allData[4][1:])
s2 = fixRange(allData[5][1:])
s3 = fixRange(allData[6][1:])
s4 = fixRange(allData[7][1:])
s5 = fixRange(allData[8][1:])
s6 = fixRange(allData[9][1:])
target = allData[10][1:]

# Perform MLR (alpha = 0.01, deltaJ = 0.01)
ThetaNumerical.changeDataPoints([age, sex, bmi, bp, s1, s2, s3, s4, s5, s6], target)
thetaList = ThetaNumerical.initializeThetaNumerical()
newThetaList = ThetaNumerical.gradientDescent(thetaList)

# Print thetas
for x in newThetaList:
    print(x)

# Calculate and print prediction values
predictedValues = ThetaNumerical.runFunction(newThetaList)

# Calculate and print r^2
determination = rSquared(predictedValues, target)
print("The data has an r^2 value of: " + str(determination))