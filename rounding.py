import numpy
import pylab
import bisect


def generateDomain(start, end, numberOfSamples):
	return numpy.linspace(start, end, numberOfSamples)

def generateRandomNumbers(domain, number, seed=None):
	# Seed the random number generator
	numpy.random.seed(seed)
	# Initialize the data array
	domainSize = domain.size
	occurences = numpy.zeros(domainSize)
	# Generate random numbers
	for i in range(0, number):
		# Find a random sample
		randomX = (int)(numpy.random.uniform(0, domainSize))
		# Increment value of that sample
		occurences[randomX] += 1
	return occurences

def findAverage(domain, samples):
	domainSize = domain.size
	numberOfSamples = 0
	weightedSum = 0
	for i in range(0, domainSize):
		weight = domain[i]
		weightedSum += samples[i] * weight
		numberOfSamples += samples[i]
	return weightedSum / numberOfSamples

def findMax(samples):
	return numpy.amax(samples)

def roundValues(domain, samples, roundToClosestEvenInt):
	domainSize = domain.size
	outputArray = numpy.zeros(domainSize)
	for sample in range(0, domainSize):
		value = domain[sample]
		roundedValue = 0
		# Round the value
		if (roundToClosestEvenInt == True):
			# Numpy is rounding to nearest even integer
			roundedValue = numpy.around(value)
		else:
			# Python is rounding to nearest integer
			roundedValue = round(value)

		# Find where in domain the rounded value resides
		roundedValueIndex = bisect.bisect(domain, roundedValue) - 1

		# Move samples from value to the rounded value
		outputArray[roundedValueIndex] += samples[value]
	return outputArray

def rmse(a, b):
	return numpy.sqrt(numpy.average((a-b)**2))	

# Configure
domainMin = 0
domainMax = 20
amountOfSamples = 10000
seed = None

# Print configuration
print 'Domain: x in [', domainMin, ',', domainMax, '], dx = 0.1. Number of samples:', amountOfSamples

# Generate domain and random numbers
domain = generateDomain(domainMin, domainMax, domainMax*10 + 1)
randomSamples = generateRandomNumbers(domain, amountOfSamples, seed)

# Perform rounding
roundedToClosestEven = roundValues(domain, randomSamples, True)
roundedToClosestInt = roundValues(domain, randomSamples, False)

averageOfRandom = findAverage(domain, randomSamples)
averageOfRoundedToClosestEven = findAverage(domain, roundedToClosestEven)
averageOfRoundedToClosestInt = findAverage(domain, roundedToClosestInt)

errorOfRoundingToClosestEven = rmse(averageOfRandom, averageOfRoundedToClosestEven)
errorOfRoundingToClosestInt = rmse(averageOfRandom, averageOfRoundedToClosestInt)

# Print output
print 'Actual average:', averageOfRandom
print 'Average after rounding to closest even integer:', averageOfRoundedToClosestEven, '(rmse =', errorOfRoundingToClosestEven, ')'
print 'Average after rounding to any closest integer:', averageOfRoundedToClosestInt, '(rmse =', errorOfRoundingToClosestInt, ')'

# This will be used to normalize the graphs
largestRandomValue = findMax(randomSamples)
largestRandomValueRoundedToClosestEven = findMax(roundedToClosestEven)
largestRandomValueRoundedToClosestInt = findMax(roundedToClosestInt)

# Plots three graphs showing random samples, 
# samples rounded to closest even int
# and samples rounded to any closest int
# Together with respective averages
pylab.figure(1)
pylab.subplot(3,1,1)
pylab.plot(domain, randomSamples / largestRandomValue) # normalize each graph
#pylab.xlabel('x')
#pylab.ylabel('y')
pylab.title('Random samples')
pylab.vlines(averageOfRandom, 0.01, 0.99, 'g') # min=0.01 and max=0.99 produce better looking graphs

pylab.subplot(3,1,2)
pylab.plot(domain, roundedToClosestEven / largestRandomValueRoundedToClosestEven)
#pylab.xlabel('x')
#pylab.ylabel('y')
pylab.title('Random samples rounded to closest even integer')
pylab.vlines(averageOfRoundedToClosestEven, 0.01, 0.99, 'k')

pylab.subplot(3,1,3)
pylab.plot(domain, roundedToClosestInt / largestRandomValueRoundedToClosestInt)
#pylab.xlabel('x')
#pylab.ylabel('y')
pylab.title('Random samples rounded to any closest integer')
pylab.vlines(averageOfRoundedToClosestInt, 0.01, 0.99, 'r')

# Plots one graph with all averages
pylab.figure(2)
pylab.plot(domain, randomSamples / largestRandomValue)

pylab.vlines(averageOfRandom, 0.01, 0.99, 'g')
pylab.vlines(averageOfRoundedToClosestEven, 0.01, 0.97, 'k')
pylab.vlines(averageOfRoundedToClosestInt, 0.01, 0.97, 'r')
pylab.title('Averages produced by various rounding techniques')

pylab.show()
