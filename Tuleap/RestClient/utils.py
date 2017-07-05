import sys


def at_least_python_3():
    return sys.hexversion >= 0x03000000


def at_least_python_33():
    return sys.hexversion >= 0x03030000
