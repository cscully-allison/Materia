import numpy as np
import pandas as pd
import math
from inspect import getsource, getargspec
from libs.Flag import Flag
from libs.Value import Value

'''
Name: TimeSeries
Description: Core data structure. Contains one vector and one TimeSeries.
'''
class TimeSeries():
    def __init__(self, values=None, index=None, timedelta=None, dtype=None, flagConf=None, flags=None, header=None):
        # check for valid input index
        self._index = np.array(index, dtype='datetime64')
        self._timedelta = None
        self._dtype = dtype
        self._header = header

        # check for valid datatypes
        # throw error if datatype does not match value
        self._values = np.array(values, dtype= 'f8' if (dtype is None) else dtype)
        self._flags = np.zeros_like(values, dtype='object')
        self._flagconf = flagConf
        self._testHist = np.array([], dtype='object')

        self._state = {}




    '''
--- Built In Test Methods ------------------------
    '''

    def reindex(self, timedelta):
        tmp = pd.DataFrame({'dtindex':self._index, 'values': self._values, 'flags':self._flags}, columns=['dtindex','values','flags'])
        td = pd.Timedelta(timedelta)

        tmp = tmp.set_index('dtindex')

        tmp = tmp.reindex(pd.date_range(start=tmp.index[0], end=tmp.index[-1], freq=td))

        self._index = tmp.index.to_numpy()
        self._values = tmp['values'].to_numpy()
        self._flags = tmp['flags'].to_numpy()




    def missingValueTest(self, mvAlias=None):

        if self._timedelta is None:
            raise Exception(
            '''
Error: Cannot test for missing values without defining series timestep length.
Please specify series timestep with <TimeSeries>.timestep().
            '''
            )

        tmp = pd.DataFrame({'dtindex':self._index, 'values': self._values, 'flags':self._flags}, columns=['dtindex','values','flags'])
        td = pd.Timedelta(self._timedelta)

        tmp = tmp.set_index('dtindex')

        tmp = tmp.reindex(pd.date_range(start=tmp.index[0], end=tmp.index[-1], freq=td))

        self._index = tmp.index.to_numpy()
        self._values = tmp['values'].to_numpy()
        self._flags = tmp['flags'].to_numpy()

        missingvals = np.argwhere(np.isnan(self._values))

        if mvAlias is not None:
            missingvals = np.append(missingvals, np.where(self._values == mvAlias))

        for i in missingvals:
            self._flags[i] = Flag(self._flagconf[self._state['flagKey']], self._flagconf['None'])


        return

    """
---- Fluent Syntax Methods ----------------------
    """



    def datapoint(self):
        return self

    def flag(self, arg):
        if self._flagconf is None:
            raise Exception("\nError: No flag codes were defined. Please define a flag code dict with DataSet.flagcodes().are().")
        elif arg not in self._flagconf.keys():
            raise Exception("\nError: Flag code key not found in dataset flag codes. Please ensure that '" + arg + "' exists in dataset flag codes.")
        self._state['flagKey'] = arg
        return self

    def flags(self):
        return self._flags

    def data(self):
        return self._values

    def when(self, funct):
        # this is important for provenance
        self._testHist = np.append(self._testHist, np.array([(self._state['flagKey'], getsource(funct))], dtype=[('test', 'U100'), ('testDef', 'U10000')]))

        iter = False
        if len(getargspec(funct)[0]) > 1:
            if 'i' in getargspec(funct)[0] or 'index' in getargspec(funct)[0]:
                iter = True;


        for i, v in enumerate(self._values):

            val = Value(i, self._values, v, self._index[i], timestep=self._timedelta)

            # switch for additional arguments
            if iter:
                ret = funct(val, i)
            else:
                ret = funct(val)

            if ret is None:
                ret = False

            if ret:
                if self._flags[i] is 0:
                    self._flags[i] = Flag(self._flagconf[self._state['flagKey']], self._flagconf['None'])
                else:
                    self._flags[i].addCode(self._flagconf[self._state['flagKey']])
            else:
                if self._flags[i] is 0:
                    self._flags[i] = Flag(self._flagconf['None'], self._flagconf['None'])

        return self

    def timestep(self, ts):
        self._timedelta = ts
        return self

    def testHistory(self):
        return self._testHist


    """
---- Sugar Functions ------------------------
    """
    def beginning(self, offset=0):
        return self._index[0 + offset]

    def end(self):
        return self._index[len(self._index)-1]

    def value(self):
        return self

    def at(self, arg):
        # reindex if necessary
        if len(self._values) != len(arg._context):
            self.reindex(arg._timedelta)

        if type(arg) is type(Value()):
            return Value(arg._valueIndex, self._values, self._values[arg._valueIndex], arg._dt, timestep=self._timedelta)

        # allow for index or timestamp



    """
---- Private Functions -----------------------
    """
