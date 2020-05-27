from Materia import *

# Create our datasets
# Performs automatic detection of column datatypes
# Sets datetime index automatically
# Stores data in column major format
DS = Dataset("data/rockland.csv", numHeaderLines=9)
DS2 = Dataset("data/evergreen.csv")
DS3 = Dataset("data/bigelow_soilMTP_2017.csv", numHeaderLines=2)

# Use existing metadata in header rows to generate unique column headers
DS.genHeadersFromMetadataRows((1,6))

# Load the flag codes assocaited with our DataSet
# Supports any flag code standard (IOOS, NOAA, etc.)
DS.flagcodes().are({"None":0, "Repeat Value":"Repeat Value", "Missing Value": "Missing", "Outlier": "Exceeds Range", "Hrdwr Range": "Exceeds Hardware Specified Range", "Spatial Inconsistency": "Incosistent (Spatial)", "Logical Inconsistency": "Inconsistent (Logical)", "Spike": "Spike"})

# Pull multiple time series objects out of our DataSet objects
series_max = DS['Air temperature (2-meter) monitor_Maximum']
series_min = DS['Air temperature (2-meter) monitor_Minimum']
series_max_10 = DS['Air temperature (10-meter) monitor_Maximum']

# Define the expected time step for our time series
# Used to find missing values and align series which are between the same dates but may have different numbers of values
series_max.timestep((series_max.beginning(+1)) - series_max.beginning())
series_min.timestep((series_min.beginning(+1)) - series_min.beginning())


'''
----------- TEST DEFINTIONS ---------------
'''

'''
Repeat Value Test.

Checks if there is a flat line in our time series.

The "value" argument is required for a test defintion.

Abstracts out a loop over our time series and allows users
    to specify tests in terms of any scalar value in our time series.
'''
def rv_test(value):
    n = 3
    if not value.isnan():
        if value == value.prior(n):
            return True
    return False

'''
Range test.

Checks if a value is in a user specified range.
'''
def range_test(value):
    USR_MAX = 28
    USR_MIN = -7.8
    return (value < USR_MIN or value > USR_MAX)

'''
Spatial Inconsistency test.

Checks if two datapoints between two spatially similar series are sufficently similar within a certian threshold.

"i" is an optional argument which gives the current index of value
'''
def spatial_inconsistency(value, i):
    comp_val = series_max_10.value().at(value)
    diff = value - comp_val
    avg = (value + comp_val) / 2
    threshold_p = 75

    exceeds_threshold = abs(diff / avg) * 100.0 > threshold_p

    if exceeds_threshold:
        return True

    return False


'''
Logical inconsistency.

Checks if two values are logically inconsistent. Eg. is a max measurement less than a min measurement.
'''
def logical_inconsistency(max_value):
    min_val = series_min.value().at(max_value)

    if min_val > max_value:
        return True

    return False

'''
Slope test.

Checks if the slope of a current value and it's value at t-1 is signficantly different than the slope between t-1 and t-n.
'''
def slope_test(value, i):
    p_a = value.prior(2)[0]
    p_b = value.prior(2)[1]
    p_c = value

    priorslp = 0.0

    if p_a.isScalar() and p_b.isScalar():
        # x values
        x1 = p_a
        x2 = p_b

        # y values
        y1 = p_a.intIndex()
        y2 = p_b.intIndex()

        # current slope
        priorslp = (y2-y1)/(x2-x1)

        # x ad y values for next point
        x3 = p_c
        y3 = p_c.intIndex()

        # next slope
        nextslp = (y3-y2)/(x3-x2)

        if (abs(nextslp) < .1                   #very sharp slope
        and abs(nextslp) < abs(priorslp*.01)    #big difference between the two slopes
        and abs(nextslp) != float("inf")        #slope is not a flat line
        and abs(priorslp) != float("inf")):     #slope is not a flat line
            return True

        return False


# checks for missing values
series_max.datapoint().flag('Missing Value').missingValueTest(-9999)

# appends flag to our time series at time t when tests return true

series_max.datapoint().flag("Repeat Value").when(rv_test)
series_max.datapoint().flag("Outlier").when(range_test).when( lambda value: (value < -100 or value > 100) )
series_max.datapoint().flag("Spatial Inconsistency").when(spatial_inconsistency)
series_max.datapoint().flag("Logical Inconsistency").when(logical_inconsistency)
series_max.datapoint().flag("Spike").when(slope_test)


# writing out results to csv
with open('rockland_flags.csv', 'w') as f:
    f.write('{},{},{}\n'.format("index", series_max._header, "{}_flags".format(series_max._header)))
    for i, dt in enumerate(series_max._index):
        f.write('{},{},{}\n'.format(dt, series_max._values[i], series_max._flags[i]))

with open('rockland_tests.csv', 'w') as f:
    for t in series_max._testHist:
        f.write('{}-------\n'.format(t[0]))
        f.write('\n{}\n'.format(t[1]))
        f.write('\n')
