import copy

#points [[0,0],[1,1]]
#function [1,0,3,1] 1+0x+3x^2+1x^3

from os import truncate


def getValue(function, x):
    val = 0.0
    power = 0
    for coef in function:
        val += coef * (x**power)
        power += 1
    return val

def getError(points, function):
    total = 0
    for point in points:
        fx = getValue(function, point[0])
        total += (fx-point[1])**2
    return total

def regressOnce(points, function):
    error = getError(points, function)
    for i in range(len(function)):
        while True:
            n = copy.deepcopy(function)
            n[i] += 0.01
            n[i] = round(n[i],2)
            newError = getError(points, function)
            if newError > error:
                break
            else:
                function = n
                error = newError
        while True:
            n = copy.deepcopy(function)
            n[i] -= 0.01
            n[i] = round(n[i],2)
            newError = getError(points, n)
            if newError > error:
                break
            else:
                function = n
                error = newError
    return function

def regress(points, times):
    function = [0,0,0,0,0]
    for i in range(100):
        function = regressOnce(points,function)
    return function


if "__main__" in __name__:
    points = [
        [-4,-1.982],
        [0,3],
        [1,5.718],
        [2,11.389],
        [3,25.086],
        [4,60.598],
    ]

    print(regress(points,100))
    