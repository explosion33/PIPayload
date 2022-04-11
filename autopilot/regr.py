# y = ae^(bt) * cos(ct + d) + h

import math


def getLocalExtrema(points):
    if (len(points) < 3):
        return 0

    extrema = []
    maxima = []
    minima = []

    prev = 0
    next = 2
    for i in range(1,len(points)-1):
        if points[i][1] > points[prev][1] and points[i][1] > points[next][1]:
            extrema.append(i)
            maxima.append(i)
        elif points[i][1] < points[prev][1] and points[i][1] < points[next][1]:
            extrema.append(i)
            minima.append(i)
        
        prev += 1
        next += 1

    return extrema, maxima, minima

def calcFrequencyShift(points):
    extrema, maxima, minima = getLocalExtrema(points)

    if (len(extrema) < 2):
        return

    PI = 3.14159

    #calculate frequency, or c coefficient

    f = extrema[0]
    sum = 0
    for val in extrema[1::]:
        sum += points[val][0] - points[f][0]
        f = val

    freq = PI / (sum / (len(extrema)-1))

    #calculate shift or d coefficient

    d1 = points[maxima[0]][0]*PI/freq*-1
    d2 = -1 - points[minima[0]][0]*PI/freq

    d1 /= PI
    d2 /= PI

    t1 = int(d1)
    t2 = int(d2)

    d1 -= t1
    d2 -= t2

    if t1 % 2 != 0:
        d1 += 1
    if t2 % 2 != 0:
        d2 += 1

    shift = (d1 + d2)/2

    return freq, shift


# y = ae^(bt) * cos(ct + d) + h
def getValue(a,b,c,d,h, t):
    E = 2.71828182846
    return (a*(E**(b*t)) * math.cos((c*t) + d)) + h

def getError(a,b,c,d,h, points):
    error = 0
    for point in points:
        fx = getValue(a,b,c,d,h, point[0])
        error += (fx-point[1])**2

    return error

def regressB(a,c,d,h, points):
    b = 0

    minError = (0,getError(a,b,c,d,h, points))

    while True:
        b -= 0.01
        e = getError(a,b,c,d,h, points)

        #print(minError, e, getValue(a,b,c,d,h, 6))

        if e < minError[1]:
            minError = (b, e)
        else:
            break
    while True:
        b += 0.01
        e = getError(a,b,c,d,h, points)

        if e < minError[1]:
            minError = (b, e)
        else:
            break

    return b


if "__main__" in __name__:
    import matplotlib.pyplot as plt
    import numpy as np
    points = [
        ( 0 , 60.0 ),
        ( 1 , 45.0 ),
        ( 2 , 27.0 ),
        ( 3 , 10.0 ),
        ( 4 , -5.0 ),
        ( 5 , -17.0 ),
        ( 6 , -20.0 ),
        ( 7 , -17.0 ),
        ( 8 , -10.0 ),
        ( 9 , -2.0 ),
        ( 10 , 4.0 ),
        ( 11 , 7.0 ),
        ( 12 , 7.6 ),
        ( 13 , 5.6 ),
        ( 14 , 2.6 ),
        ( 15 , -1.6 ),
        ( 16 , -3.0 ),
        ( 17 , -3.5 ),
        ( 18 , -2.9 ),
        ( 19 , -1.6 ),
        ( 20 , 0.0 ),
        ( 21 , 1.0 ),
        ( 22 , 1.5 ),
        ( 23 , 1.45 ),
        ( 24 , 1.05 ),
        ( 25 , 0.55 ),
        ( 26 , 0.0 ),
        ( 27 , -0.4 ),
    ]

    a = (points[0][1])/math.cos(points[0][0])
    c, d = calcFrequencyShift(points)
    h = 0

    b = regressB(a,c,d,h, points)

    print(a,b,c,d,h)

    x = []
    y = []
    i = points[0][0]
    while i <  points[len(points)-1][0]:
        x.append(i)
        y.append(getValue(a,b,c,d,h,i))
        i += 0.05

    x = np.array(x)
    y = np.array(y)


    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    ax.spines['bottom'].set_position('zero')

    plt.plot(x,y)

    x = []
    y = []
    for point in points:
        x.append(point[0])
        y.append(point[1])

    x = np.array(x)
    y = np.array(y)

    # plot the function
    plt.plot(x,y, 'o')
    
    # show the plot
    plt.show()



