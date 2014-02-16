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

def findSumAndAverage(domain, samples):
	domainSize = domain.size
	numberOfSamples = 0
	weightedSum = 0
	for i in range(0, domainSize):
		weight = domain[i]
		weightedSum += samples[i] * weight
		numberOfSamples += samples[i]
	return (weightedSum, weightedSum / numberOfSamples)

def findMax(samples):
	return numpy.amax(samples)

def roundValues(domain, samples, roundToClosestEvenInt):
	domainSize = domain.size
	outputArray = numpy.zeros(domainSize)
	for sample in range(0, domainSize):
		value = domain[sample]
		roundedValue = 0
		# Round the value
		# TODO: instead of using numpy or python's implementation,
		#       I should do rounding on my own.
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
parser = argparse.ArgumentParser(description='Demonstrate difference between rounding half up and rounding half to even (banker\'s rounding')
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
# Safety
if (domainMin >= domainMax):
	parser.print_help()
	exit(1)

# Print configuration
print 'Domain: x in [', domainMin, ',', domainMax, '], dx = 0.1. Number of samples:', amountOfSamples

# Generate domain and random numbers
# Amount of samples=domainMax*10 + 1 ensures that dx=0.1
domain = generateDomain(domainMin, domainMax, (domainMax-domainMin)*10 + 1)
randomSamples = generateRandomNumbers(domain, amountOfSamples, seed)

# Perform rounding
roundedToClosestEven = roundValues(domain, randomSamples, True)
roundedToClosestInt = roundValues(domain, randomSamples, False)

# Find metrics
sumOfRandom, averageOfRandom = findSumAndAverage(domain, randomSamples)
sumOfRoundedToClosestEven, averageOfRoundedToClosestEven = findSumAndAverage(domain, roundedToClosestEven)
sumOfRoundedToClosestInt, averageOfRoundedToClosestInt = findSumAndAverage(domain, roundedToClosestInt)

# Find errors
errorAvgEven = percentError(averageOfRandom, averageOfRoundedToClosestEven)
errorAvgInt = percentError(averageOfRandom, averageOfRoundedToClosestInt)
errorSumEven = percentError(sumOfRandom, sumOfRoundedToClosestEven)
errorSumInt = percentError(sumOfRandom, sumOfRoundedToClosestInt)

# Print output
print 'Actual average:', averageOfRandom
print 'Average after rounding half to even:', averageOfRoundedToClosestEven, '. Error =', errorAvgEven, '%'
print 'Average after rounding half up:', averageOfRoundedToClosestInt, '. Error =', errorAvgInt, '%'
print 'Actual sum:', sumOfRandom
print 'Sum after rounding half to even:', sumOfRoundedToClosestEven, '. Error =', errorSumEven, '%'
print 'Sum after rounding half up:', sumOfRoundedToClosestInt, '. Error =', errorSumInt, '%'

if (numpy.abs(sumOfRandom - sumOfRoundedToClosestInt) < numpy.abs(sumOfRandom - sumOfRoundedToClosestEven)):
	print 'Here, rounding half up is a better method'
elif (sumOfRoundedToClosestEven == sumOfRoundedToClosestInt):
	print 'Here, both rounding methods are equally as good'
else:
	print 'Here, rounding half to even is a better method'

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
	pylab.bar(domain, randomSamples, width=0.1, color='g', alpha=0.4)
	pylab.title('Random samples. avg = ' + str(averageOfRandom) + ' sum = ' + str(sumOfRandom))
	pylab.vlines(averageOfRandom, 0.01, 0.99 * largestRandomValue, 'g') # min=0.01 and max=0.99 produce better looking graphs

	pylab.subplot(3,1,2)
	pylab.bar(domain, roundedToClosestEven, width=0.1 , color='b', alpha=0.4)
	pylab.title('Rounding half to even. avg = ' + str(averageOfRoundedToClosestEven) + ' sum = ' + str(sumOfRoundedToClosestEven))
	pylab.vlines(averageOfRoundedToClosestEven, 0.01, 0.99 * largestRandomValueRoundedToClosestEven, 'k')

	pylab.subplot(3,1,3)
	pylab.bar(domain, roundedToClosestInt, width=0.1, color='r', alpha=0.4)
	pylab.title('Rounding half up. avg = ' + str(averageOfRoundedToClosestInt) + ' sum = ' + str(sumOfRoundedToClosestInt))
	pylab.vlines(averageOfRoundedToClosestInt, 0.01, 0.99 * largestRandomValueRoundedToClosestInt, 'r')

	# Plots one graph with all averages
	pylab.figure(2)
	pylab.bar(domain, randomSamples / largestRandomValue, width=0.1, color='g', alpha=0.4) # normalize the graph

	pylab.vlines(averageOfRandom, 0.01, 0.99, 'g')
	pylab.vlines(averageOfRoundedToClosestEven, 0.01, 0.97, 'k')
	pylab.vlines(averageOfRoundedToClosestInt, 0.03, 0.99, 'r')
	pylab.title('Averages after rounding: half up - red, and half to even - black')

	pylab.show()
