import numpy
import pylab
import bisect
import argparse

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

		# Safety
		if (numpy.abs(roundedValue - value) > 0.5):
			print "ERROR: Incorrect rounding of", value, "to", roundedValue

		# Find where in domain the rounded value resides
		roundedValueIndex = bisect.bisect(domain, roundedValue) - 1

		# Safety
		if (roundedValue != domain[roundedValueIndex]):
			print "ERROR: Found roundedValue", roundedValue, "in domain [", roundedValueIndex, "], but the value is", domain[roundedValueIndex]

		# Move samples from value to the rounded value
		outputArray[roundedValueIndex] += samples[sample]
	return outputArray

def percentError(experimental, actual):
	return numpy.abs(experimental - actual) / actual * 100

# Parse arguments
parser = argparse.ArgumentParser(description='Demonstrate difference between rounding to nearest integer and rounding to nearest even integer')
parser.add_argument('domainMin', type=int, nargs='?', default=0,
                   help='Lower bound on the domain (inclusive). Default = 0')
parser.add_argument('domainMax', type=int, nargs='?', default=10,
                   help='Upper bound on the domain (inclusive). Default = 10')
parser.add_argument('samples', type=int, nargs='?', default=10000,
                   help='Number of samples to generate. Default = 10000')
parser.add_argument('--plot', type=int, nargs='?', default=1,
                   help='0 to supress plot creation. Default = 1')
parser.add_argument('--seed', type=int, nargs='?', default=None,
                   help='Seed for the random number generator. Default = None')

args = parser.parse_args()
# Configure
domainMin = args.domainMin
domainMax = args.domainMax
amountOfSamples = args.samples
seed = args.seed
createPlots = args.plot

# Print configuration
print 'Domain: x in [', domainMin, ',', domainMax, '], dx = 0.1. Number of samples:', amountOfSamples

# Generate domain and random numbers
# Amount of samples=domainMax*10 + 1 ensures that dx=0.1
domain = generateDomain(domainMin, domainMax, domainMax*10 + 1)
randomSamples = generateRandomNumbers(domain, amountOfSamples, seed)

# Perform rounding
roundedToClosestEven = roundValues(domain, randomSamples, True)
roundedToClosestInt = roundValues(domain, randomSamples, False)

averageOfRandom = findAverage(domain, randomSamples)
averageOfRoundedToClosestEven = findAverage(domain, roundedToClosestEven)
averageOfRoundedToClosestInt = findAverage(domain, roundedToClosestInt)

errorOfRoundingToClosestEven = percentError(averageOfRandom, averageOfRoundedToClosestEven)
errorOfRoundingToClosestInt = percentError(averageOfRandom, averageOfRoundedToClosestInt)

# Print output
print 'Actual average:', averageOfRandom
print 'Average after rounding to closest even integer:', averageOfRoundedToClosestEven, '. Error =', errorOfRoundingToClosestEven, '%'
print 'Average after rounding to any closest integer:', averageOfRoundedToClosestInt, '. Error =', errorOfRoundingToClosestInt, '%'
if (numpy.abs(averageOfRandom - averageOfRoundedToClosestInt) < numpy.abs(averageOfRandom - averageOfRoundedToClosestEven)):
	print 'Here, averaging to any closest integer is a better method'
elif (averageOfRoundedToClosestEven == averageOfRoundedToClosestInt):
	print 'Here, both rounding methods are equally as good'
else:
	print 'Here, averaging to closest even integer is a better method'

if (createPlots != 0):
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
	pylab.title('Random samples. Average = ' + str(averageOfRandom))
	pylab.vlines(averageOfRandom, 0.01, 0.99, 'g') # min=0.01 and max=0.99 produce better looking graphs

	pylab.subplot(3,1,2)
	pylab.plot(domain, roundedToClosestEven / largestRandomValueRoundedToClosestEven)
	pylab.title('Rounded to closest even integer. Average = ' + str(averageOfRoundedToClosestEven))
	pylab.vlines(averageOfRoundedToClosestEven, 0.01, 0.99, 'k')

	pylab.subplot(3,1,3)
	pylab.plot(domain, roundedToClosestInt / largestRandomValueRoundedToClosestInt)
	pylab.title('Rounded to any closest integer. Average = ' + str(averageOfRoundedToClosestInt))
	pylab.vlines(averageOfRoundedToClosestInt, 0.01, 0.99, 'r')

	# Plots one graph with all averages
	pylab.figure(2)
	pylab.plot(domain, randomSamples / largestRandomValue)

	pylab.vlines(averageOfRandom, 0.01, 0.99, 'g')
	pylab.vlines(averageOfRoundedToClosestEven, 0.01, 0.97, 'k')
	pylab.vlines(averageOfRoundedToClosestInt, 0.03, 0.99, 'r')
	pylab.title('Averages after rounding to nearest integer: any - red, and even - black')

	pylab.show()
