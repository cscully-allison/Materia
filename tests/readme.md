# Test Documentation

In this readme you will find a side by side comparison of tests written in Materia and Pandas. This is a supplemental document to the paper accepted to the QOD 2020 workshop.

# Range Test

<table>
<tr>
<th>
Pandas
</th>
<th>
Materia
</th>
</tr>

<tr>
<td>
<pre>
{
def runTest (self, dataframe):
      outdf = np.logical_and(dataframe[self.column] < self.max, dataframe[self.column] > self.min)
      return outdf.apply(lambda x: self.flag.flag(x, self.testName))
}
</pre>
</td>
<td>
<pre>
def range_test(value):
    return (value < -20 or value > 20)
</pre>
</td>
</tr>
</table>


# Persistence

<table>
<tr>
<th>
Pandas
</th>
<th>
Materia
</th>
</tr>

<tr>
<td>
<pre>
def runTest(self, dataframe):
      dfcopy = dataframe.copy()

      # get repeating or unique ids for repeating values
      dfcopy['cumsum'] = (dfcopy[self.column] != dfcopy[self.column].shift(1)).cumsum()

      # group all values by count of cumsum "id"
      # and filter down to only incidents of repeat value
      counts = dfcopy[['cumsum',self.column]].groupby(['cumsum']).agg('count')
      counts_less = counts.loc[counts[self.column] > 1]

      # join the multiple counts back to the main df
      dfcopy = dfcopy.join(counts_less, on='cumsum', lsuffix='_caller', rsuffix='_other')

      # load our original values with booleans expressing if they exceed the threshold or not
      dfcopy[self.column] = dfcopy[self.column + '_other'].map(lambda x: x >= self.threshold)


      # not x for now. Need to align the true false across datatypes
      return dfcopy[self.column].apply(lambda x: self.flag.flag((not x), self.testName))
</pre>
</td>
<td>
<pre>
def rv_test(value):
    n = 3
    if not value.isnan():
        if value == value.prior(n):
            return True
    return False

</pre>
</td>
</tr>
</table>

# Spatial Inconsistency

<table>
<tr>
<th>
Pandas
</th>
<th>
Materia
</th>
</tr>

<tr>
<td>
<pre>
def runTest(self, dataframe):
      outdf = np.abs(dataframe[self.column] - dataframe[self.comparisonColumn]) / \\
            ((dataframe[self.column]+dataframe[self.comparisonColumn]/2.0)) * \\
            100.0 < self.percentDifference
      outdf.name = self.column

      return outdf.apply(lambda x: self.flag.flag(x, self.testName))
</pre>
</td>
<td>
<pre>
def spatial_inconsistency(value, i):
    comp_val = series_max_10.value().at(value)
    threshold = abs(value * 2)

    if comp_val > (value + threshold) or comp_val < (value - threshold):
        return True

    return False

</pre>
</td>
</tr>
</table>


# Internal Inconsistency

<table>
<tr>
<th>
Pandas
</th>
<th>
Materia
</th>
</tr>

<tr>
<td>
<pre>
def runTest(self, dataframe):
      outdf = pd.DataFrame()

      if 'Max > Min' in self.comparison:
          true = np.empty_like(dataframe[self.column], dtype=bool)
          false = np.empty_like(dataframe[self.column], dtype=bool)

          # fill true and false
          true.fill(1)
          false.fill(0)

          outdf[self.column] = np.where( \\
                  (dataframe[self.column] > dataframe[self.comparisonColumn]), \\
                  true, \\
                  false)
          # print(outdf)

      outdf.name = self.column

      return outdf[self.column].apply(lambda x: self.flag.flag(x, self.testName))
</pre>
</td>
<td>
<pre>
def logical_inconsistency_min(min_value):
    max_value = series_max.value().at(min_value)

    if min_value > max_value:
        return True

    return False
</pre>
</td>
</tr>
</table>


# Change in Slope

<table>
<tr>
<th>
Pandas
</th>
<th>
Materia
</th>
</tr>

<tr>
<td>
<pre>
def runTest (self, dataframe):
      outdf = pd.DataFrame()

      # calc rise over run
      outdf[self.column] = dataframe[self.column].rolling(5).std()

      true = np.empty_like(dataframe[self.column], dtype=bool)
      false = np.empty_like(dataframe[self.column], dtype=bool)

      # fill true and false
      true.fill(1)
      false.fill(0)

      return
</pre>
</td>
<td>
<pre>
# compares slopes between values
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

</pre>
</td>
</tr>
</table>
