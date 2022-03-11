#polynomial function is y=A+Bx+Cx^2 etc represented by [A,B,C,D]

def integral0_x(function):
    div = 1
    for i in range(len(function)):
        function[i] = function[i]/div
        div += 1
    
    return [0] + function


def dervivative(function):
    function = function[1::]
    mult = 1
    for i in range(len(function)):
        function[i] = function[i]*mult
        mult += 1
    return function

def mult(function, m):
    for i in range(len(function)):
        function[i]*=m
    return function

def add(func1, func2):
    a =func1
    b= func2
    if len(func2)> len(func1):
        a = func2
        b = func1

    for i in range(len(b)):
        a[i] += b[i]

    return a

def addp(*args):
    func = []
    for f in args:
        func = add(func,f)
    return func
