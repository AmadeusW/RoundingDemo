RoundingDemo
============

After seeing https://stackoverflow.com/questions/977796/why-does-math-round2-5-return-2-instead-of-3-in-c I wanted to see the effects of Banker's Rounding.

Usage
-----
```
rounding.py [-h] [--plot [PLOT]] [--seed [SEED]]
               [domainMin] [domainMax] [samples]
```
All arguments have default values and all can be changed. **rounding.py -h** explains each argument in greater detail.

**Sample usage:**
```
$ python rounding.py
$ python rounding.py -5 5 300
$ python rounding.py 10000 20000 100000 --plot 0
```

Results
-------

*Banker's Rounding*, also known as *rounding half to even* results in smaller error of average and sum than *rounding half up*. The improvement is visible for experiments with large sample numbers. 

**Example with varying number of samples:**
```
Domain: x in [ 0 , 4 ], dx = 0.1. Number of samples: 50
Actual average: 1.86
Average after rounding half to even: 1.8 . Error = 3.33333333333 %
Average after rounding half up: 1.9 . Error = 2.10526315789 %
Actual sum: 93.0
Sum after rounding half to even: 90.0 . Error = 3.33333333333 %
Sum after rounding half up: 95.0 . Error = 2.10526315789 %
Here, rounding half up is a better method
```
<img src="https://raw.github.com/AmadeusW/RoundingDemo/master/results/rounding_0_4_50_halfUpBetter.png" />

```
Domain: x in [ 0 , 4 ], dx = 0.1. Number of samples: 200
Actual average: 2.07
Average after rounding half to even: 2.065 . Error = 0.242130750605 %
Average after rounding half up: 2.115 . Error = 2.12765957447 %
Actual sum: 414.0
Sum after rounding half to even: 413.0 . Error = 0.242130750605 %
Sum after rounding half up: 423.0 . Error = 2.12765957447 %
Here, rounding half to even is a better method
```
<img src="https://raw.github.com/AmadeusW/RoundingDemo/master/results/rounding_0_4_200_halfToEvenBetter.png" />

```
Domain: x in [ 0 , 4 ], dx = 0.1. Number of samples: 2000
Actual average: 1.9737
Average after rounding half to even: 1.985 . Error = 0.569269521411 %
Average after rounding half up: 2.025 . Error = 2.53333333333 %
Actual sum: 3947.4
Sum after rounding half to even: 3970.0 . Error = 0.569269521411 %
Sum after rounding half up: 4050.0 . Error = 2.53333333333 %
Here, rounding half to even is a better method
```
<img src="https://raw.github.com/AmadeusW/RoundingDemo/master/results/rounding_0_4_2000_halfToEvenBetter.png" />

**Example with negative numbers:**
```
Domain: x in [ -5 , 5 ], dx = 0.1. Number of samples: 100
Actual average: -0.225
Average after rounding half to even: -0.24 . Error = -6.25 %
Average after rounding half up: -0.28 . Error = -19.6428571429 %
Actual sum: -22.5
Sum after rounding half to even: -24.0 . Error = -6.25 %
Sum after rounding half up: -28.0 . Error = -19.6428571429 %
Here, rounding half to even is a better method
```
<img src="https://raw.github.com/AmadeusW/RoundingDemo/master/results/rounding_-5_5_100_halfToEvenBetter.png" />
```
