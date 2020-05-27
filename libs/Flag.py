
'''
Name: Flag
Description: An object which holds metadata about a flagged datapoint.
Private Members: Flag code, test Parameters/defintion
'''
class Flag():
    def __init__(self, code, noneCode, timestamp=None):
        self._codes = [code]
        self._noneCode = noneCode
        self._timestamp = timestamp

    def __iadd__(self, other):
        return __add__(other)

    def __add__(self, other):
        if self._codes == other._codes:
            return self._codes

        elif len(self._codes) is 1 and self._noneCode in self._codes:
            return Flag(other._codes, other._noneCode, other._timestamp)

        elif (self._noneCode not in self._codes and
         other._noneCode not in other._codes):
            tmp = deepcopy(self._codes)
            for c in other._codes:
                tmp.append(c)
            return tmp

    def addCode(self, code):
        # if we only have noneCode
        if len(self._codes) is 1 and self._noneCode in self._codes:
            self._codes[0] = code
        if code in self._codes:
            return
        if code is self._noneCode:
            return
        else:
            self._codes.append(code)

    def isFlag(self, flag):
        if flag in self._codes:
            return True
        return False

    def notNone(self):
        if self._noneCode in self._codes:
            return False
        return True

    def __str__(self):
        if len(self._codes) is 1:
            return str(self._codes[0])
        return str(self._codes)
