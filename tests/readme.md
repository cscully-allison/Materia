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
