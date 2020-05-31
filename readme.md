# Materia

Materia is an Embedded Domain Specific Language written in Python which provides tools and abstractions to simplify creation and execution of quality control tests on your tabular data sets.

## Installation

To install and use Materia, clone this repository to your local machine. Navigate to the top-level Materia directory and run,

```
pip3 install -r requirements.txt
```

After this, copy Materia.py and the libs directory to your project directory.
From there, Materia can be pulled into your data testing script with the command:

```
from Materia import *
```

This will allow you to create a new Dataset object from tabular data stored in .csv format and begin using Materia.

## Test Documenation

For a side-by-side documenation of tests evaluated in the QOD 2020 Materia paper please  [go here | https://github.com/cscully-allison/Materia/blob/master/tests/readme.md#test-documentation]


## Some Important Language Constructs


| Language Construct                   | Additional Info                               | Description                                                                                                                                                                                                                                                                                                                                  |
|--------------------------------------|--------------------------------------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Dataset()                            | args: filename <string>, numHeaderLines <int> | Dataset Constructor: reads in .csv file, load header lines in as metadata and performs automatic type conversion/detection.                                                                                                                                                                                                                  |
| Dataset.genHeadersFromMetadata()     | args: sourceRows <tuple <int>>                | Aggregates select header rows into single-line header names, for intuitive time-series dereferencing.                                                                                                                                                                                                                                        |
| Dataset.flagcodes().are()            | args: dict <str or int>                       | Associates a particular set of flag codes with a dataset. These are invoked during testing and define what flags will be output by a non-passing test of a particular type.                                                                                                                                                                  |
| Timeseries.timestep()                | args: ts <timedelta>                          | Sets the expected timestep between two values in the tested dataset. This is used in missing values tests and aligning timer series with different numbers of rows.                                                                                                                                                                          |
| Test Definition                      |                                               | A test definition works by defining a normal python function with two special arguments: "value" and "i". The value argument represents an arbitrary data value in your tested time series. These special "test defintion" functions are written to perform some test against this arbitrary variable and its temporally adjacent neighbors. |
| Value                                |                                               | The "value" variable passed into a test definition is an object which holds either an integer, float or list of those datatypes. It overloads all common math operators to allow for most scalar/vector arithmetic which may be required for test definitions.                                                                               |
| Timeseries.datapoint().flag().when() | flag(fName <string>), when(funct <function>)  | This chained method call enables users to invoke special test definitions (funct) to operate on all values over the calling timeseries.  Flags are matched to the dictionary set in a prior flagcodes().are() call. This function automatically creates a time-stamp aligned column of QC flags associated with the calling time series.     |
