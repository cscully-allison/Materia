import math
import numpy as np

supress = True

class Value():
    def __init__(self, valueNdx=None, context=None, currentValue=None, dt=None, scalar=True, timestep=None):
        self._valueIndex = valueNdx
        self._dt = dt
        self._context = context
        self.value = currentValue
        self._scalar = scalar
        self._timedelta = timestep


    def isnan(self):
        return math.isnan(self.value)

    def isScalar(self):
        return self._scalar

    def intIndex(self):
        return self._valueIndex

    def dateTimeIndex(self):
        return self._dt

    def prior(self, num):
        if (self._valueIndex - num) < 0:
            sublist = np.empty([0])
            if not supress:
                print("Warning: Value.prior() specified number out of bounds, empty array returned.")
            if self._scalar is False:
                raise Exception('''Cannot get prior from list. Please use this function only on the original value variable.''')
            if self._context is None:
                raise Exception('''Cannot get prior derived math product. Please use this function only on the original value variable or one pulled from a time series using the .at() function.''')
        else:
            sublist = self._context[self._valueIndex-num:self._valueIndex]
        return Value(self._valueIndex-num, sublist, self.value, self._dt, False, timestep=self._timedelta)


    """
    Overloaded Operators
    """
    def __getitem__(self, key):
        if type(key) is type(0) and self._scalar is False:
            if len(self._context) <= key:
                return self
            return Value(self._valueIndex + key, self._context, self._context[key], self._dt, True, timestep=self._timedelta)

    def __contains__(self, key):
        pass

    def __add__(self, other):
        if type(self) is type(other):
            return self._mathOrganizer(self, other, '+')
        else:
            if type(other) is not type("") and type(other) is not type({}):
                return Value(currentValue=self.value + other)

    def __radd__(self, other):
        return self.__add__(other)

    def __sub__(self, other):
        if type(self) is type(other):
            return self._mathOrganizer(self, other, '-')
        else:
            if type(other) is not type("") and type(other) is not type({}):
                return Value(currentValue=self.value - other)

    def __rsub__(self, other):
        if type(self) is type(other):
            return self._mathOrganizer(other, self, '-')
        else:
            if type(other) is not type("") and type(other) is not type({}):
                return Value(currentValue= other - self.value)

    def __mul__(self, other):
        if type(self) is type(other):
            return self._mathOrganizer(self, other, '*')
        else:
            if type(other) is not type("") and type(other) is not type({}):
                return Value(currentValue= other * self.value)

    def __rmul__(self, other):
        return self.__mul__(other)

    def __truediv__(self, other):
        if type(self) is type(other):
            return self._mathOrganizer(self, other, '/')
        elif type(other) is not type("") and type(other) is not type({}):
            if self._scalar is False:
                return self._mathOrganizer(self, Value(currentValue=other), '/')
            else:
                return Value(currentValue= self.value / other)

    def __floordiv__(self, other):
        if type(self) is type(other):
            return self._mathOrganizer(self, other, '/')
        elif type(other) is not type("") and type(other) is not type({}):
            if self._scalar is False:
                return self._mathOrganizer(self, Value(currentValue=other), '/')
            else:
                return Value(currentValue= self.value // other)
    #
    # def __div__(self, other):
    #     if type(self) is type(other):
    #         return self._mathOrganizer(self, other, '/')
    #     else:
    #         if type(other) is not type("") and type(other) is not type({}):
    #             return Value(currentValue= self.value / other)
    #
    # def __rdiv__(self, other):
    #     if type(self) is type(other):
    #         return self._mathOrganizer(other, self, '/')
    #     else:
    #         if type(other) is not type("") and type(other) is not type({}):
    #             return Value(currentValue= other / self.value)

    # overloaded comparision operators
    def __gt__(self, other):

        if type(self) is type(other):
            return self._comparisionOrganizer(other, ">")
        else:
            if type(other) is not type("") and type(other) is not type({}):
                return self.value > other

    def __ge__(self, other):
        if type(self) is type(other):
            return self._comparisionOrganizer(other, ">=")
        else:
            if type(other) is not type("") and type(other) is not type({}):
                return self.value >= other

    def __lt__(self, other):
        if type(self) is type(other):
            return self._comparisionOrganizer(other, "<")
        else:
            if type(other) is not type("") and type(other) is not type({}):
                return self.value < other

    def __le__(self, other):
        if type(self) is type(other):
            return self._comparisionOrganizer(other, "<=")
        else:
            if type(other) is not type("") and type(other) is not type({}):
                return self.value <= other

    def __ne__(self, other):
        if type(self) is type(other):
            return self._comparisionOrganizer(other, "!=")
        else:
            if type(other) is not type("") and type(other) is not type({}):
                return self.value != other

    def __eq__(self, other):
        if type(self) is type(other):
            return self._comparisionOrganizer(other, "==")
        else:
            if type(other) is not type("") and type(other) is not type({}):
                return self.value == other

    def __str__(self):
        if self._scalar is True:
            return str(self.value)
        else:
            return np.array2string(self._context)

    """
----Private functions------------
    """
    def _mathOrganizer(self, lhs, rhs, op):
        if op == "-" or op == "/":
            if lhs._scalar is True and rhs._scalar is False:
                raise Exception('''
Cannot subtract or divide a vector or list from a scalar.
                ''')
        if lhs._scalar is True and rhs._scalar is True:
            return self._scalarOp(lhs.value, rhs.value, op)
        elif lhs._scalar is True and rhs._scalar is False:
            return self._scalarListOp(lhs.value, rhs._context, op)
        elif lhs._scalar is False and rhs._scalar is True:
            return self._scalarListOp(rhs.value, lhs._context, op)
        else:
            return self._listListOp(rhs._context, lhs._context, op)
            raise Exception('''
Error: No operation defintion exists for list value {} list value within test scope.
        '''.format(op))

    def _comparisionOrganizer(self, other, cmp):
        if self._scalar is True and other._scalar is True:
            return self._scalarCmp(self.value, other.value, cmp)
        elif self._scalar is True and other._scalar is False:
            return self._scalarListCmp(self.value, other._context, cmp)
        elif self._scalar is False and other._scalar is True:
            return self._scalarListCmp(other.value, self._context, cmp)
        else:
            return self._listListCmp(other._context, self._context, cmp)


    def _scalarOp(self, lhs, rhs, op):
        if op is "+":
            return lhs + rhs
        if op is "-":
            return lhs - rhs
        if op is "*":
            return lhs * rhs
        if op is "/":
            return lhs / rhs

    def _listListOp(self, lhs, rhs, op):
        lr = []
        if op is "+":
            lr = [a + b for a, b in zip(lhs, rhs)]
        if op is "-":
            lr = [a - b for a, b in zip(lhs, rhs)]
        if op is "*":
            lr = [a * b for a, b in zip(lhs, rhs)]
        if op is "/":
            lr = [a / b for a, b in zip(lhs, rhs)]
        lrl = Value(currentValue=self.value, context=np.array(lr), scalar=False)
        return lrl

    def _scalarListOp(self, s1, l1, op):
        lr = []
        if op is "+":
            for s in l1:
                lr.append(s+s1)
        if op is "-":
            for s in l1:
                lr.append(s-s1)
        if op is "*":
            for s in l1:
                lr.append(s*s1)
        if op is "/":
            for s in l1:
                lr.append(s/s1)
        lrl = Value(currentValue=self.value, context=np.array(lr), scalar=False)
        return lrl

    def _scalarCmp(self, s1, s2, cmp):
        if cmp is "==":
            return s1 == s2
        if cmp is "<":
            return s1 < s2
        if cmp is ">":
            return s1 > s2
        if cmp is ">=":
            return s1 >= s2
        if cmp is "<=":
            return s1 <= s2
        if cmp is "!=":
            return s1 != s2
        pass

    """
    Function: _scalarListCmp
    Desc: Performs pairwise compairisions of l1 against s1. If any pair fails this
        comparision then the entire function returns false. Otherwise it returns true.
        Generally we want to flag when function returns true.
    """
    def _scalarListCmp(self, s1, l1, cmp):
        if l1.size is 0:
            return False
        elif cmp == "==":
            for val in l1:
                if s1 != val:
                    return False
            return True
        elif cmp == "<":
            for val in l1:
                if s1 >= val:
                    return False
            return True
        elif cmp == ">":
            for val in l1:
                if s1 <= val:
                    return False
            return True
        elif cmp == ">=":
            for val in l1:
                if s1 < val:
                    return False
            return True
        elif cmp == "<=":
            for val in l1:
                if s1 > val:
                    return False
            return True
        elif cmp == "!=":
            for val in l1:
                if s1 == val:
                    return False
            return True

    def _listListCmp(self, l1, l2, cmp):
        if cmp is "==":
            if l1 is l2:
                return True
            for val_a in l1:
                for val_b in l2:
                    if val_a != val_b:
                        return False
            return True

        elif cmp == "<":
            for val_a in l1:
                for val_b in l2:
                    if val_a >= val_b:
                        return False
            return True

        elif cmp == ">":
            for val_a in l1:
                for val_b in l2:
                    if val_a <= val_b:
                        return False
            return True

        elif cmp == ">=":
            for val_a in l1:
                for val_b in l2:
                    if val_a < val_b:
                        return False
            return True

        elif cmp == "<=":
            for val_a in l1:
                for val_b in l2:
                    if val_a > val_b:
                        return False
            return True

        elif cmp == "!=":
            if len(l1) != len(l2):
                return true
            for i, val_a in enumerate(l1):
                for val_b in l2:
                    if val_a == val_b:
                        return False
            return True
