value = {}

def rep_fun(func):
    class Snippet(object):
        def __init__(self):
            self.original = func
    return Snippet


class A():
    def __init__(self):
        self._callChain = []

    def m1(self, arg):
        def _actual_logic():
            print(arg)
        self._callChain.append(_actual_logic)
        return self

    def m2(self):
        print("m2")
        return self

    def run(self):
        for f in self._callChain:
            f()


def m1(arg):
    print(arg)
    x = 3
    print(arg(3))


m1(lambda x: x is 4)
