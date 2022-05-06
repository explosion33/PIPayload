# y = ae^(bt) * cos(ct + d) + h
import math
import matplotlib.pyplot as plt
import numpy as np

class ODE2Regr():
    def __init__(this):
        this._last = None
        this._lastpoints = None

    def _getLocalExtrema(this, points):
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
 

    def _calcFrequencyShift(this, points):
        extrema, maxima, minima = this._getLocalExtrema(points)

        if (len(extrema) < 2):
            return

        PI = 3.14159

        # calculate frequency, or c coefficient
        # gets the average frequency for two adjacent peaks
        # p2[x] - p1[x]/2PI is the frequency given two peaks
        ftot = 0
        num = 0
        for i in range(1,len(maxima)):
            p1 = points[maxima[i-1]]
            p2 = points[maxima[i]]

            ftot += (p2[0]-p1[0])
            num += 1

        for i in range(1,len(minima)):
            p1 = points[minima[i-1]]
            p2 = points[minima[i]]

            ftot += (p2[0]-p1[0])
            num += 1

        if num == 0:
            return (0,0) 

        avgPeakDis = ftot/num
        freq = (2*PI)/avgPeakDis

        #calculate shift or d coefficient

        tot = 0
        num = 0
        for p in maxima:
            px = points[p][0]
            low = None
            for i in range(-2,2*(len(maxima)+2), 2):
                noshift = (PI*i)/freq
                print("    ", noshift)
                if low == None or abs(noshift-px) < abs(low-px):
                    low = noshift
            print(px, low)
            tot += px - low
            num += 1
        
        for p in minima:
            px = points[p][0]
            low = None
            for i in range(-1,2*(len(minima)+2), 2):
                noshift = (PI*i)/freq
                print("    ", noshift)
                if low == None or abs(noshift-px) < abs(low-px):
                    low = noshift
            print(px, low)
            tot += px - low
            num += 1
        

        shift = tot/num

        print(tot/num, freq, shift)

        return (freq, shift)


    # y = ae^(bt) * cos(ct + d) + h
    def _getValue(this, a,b,c,d,h, t):
        E = 2.71828182846
        return (a*(E**(b*t)) * math.cos((c*t) + d)) + h


    def _getAverageHieght(this, points):
        tot = 0
        for point in points:
            tot += point[1]
        return tot/len(points)

    def _getStandardDeviation(this, points, mean=None):
        mean = this._getAverageHieght(points) if mean is None else mean

        total = 0
        for point in points:
            y = point[1]
            total += (mean-y)**2
        total /= len(points)
        total = math.sqrt(total)
        return total

    def _removeOutliers(this, points):
        mean = this._getAverageHieght(points)
        sd = this._getStandardDeviation(points, mean)
        return [point for point in points if abs(point[1]-mean) < abs(sd)]

    def _getError(this, a,b,c,d,h, points):
        error = 0
        for point in points:
            fx = this._getValue(a,b,c,d,h, point[0])
            error += (fx-point[1])**2

        return error


    def _regressB(this, a,c,d,h, points):
        points = this._removeOutliers(points)
        points = this._removeOutliers(points)
        for point in points:
            print(point)

        b = 0

        minError = (0,this._getError(a,b,c,d,h, points))

        while True:
            b -= 0.01
            e = this._getError(a,b,c,d,h, points)

            #print(minError, e, getValue(a,b,c,d,h, 6))

            if e < minError[1]:
                minError = (b, e)
            else:
                break
        while True:
            b += 0.01
            e = this._getError(a,b,c,d,h, points)

            if e < minError[1]:
                minError = (b, e)
            else:
                break

        return b


    def regress(this, points):
        a = (points[0][1])/math.cos(points[0][0])
        c, d = this._calcFrequencyShift(points)

        d *= -1

        if a < 0:
            d = 3.14159 - d

        h = 0
        b = this._regressB(a,c,d,h, points)


        this._last = [a,b,c,d,h]
        this._lastpoints = points
        return this._last

    def getEquation(this, coefs=None):
        if coefs == None:
            coefs = this._last

        a,b,c,d,h = coefs
        return "y = {}e^({}t) * cos({}t + {}) + {}".format(round(a,5),round(b,5),round(c,5),round(d,5),round(h,5))
    
    def getDesmosEquation(this, coefs=None):
        if coefs == None:
            coefs = this._last

        a,b,c,d,h = coefs
        a = str(a)
        b = str(b)
        c = str(c)
        d = str(d)
        h = str(h)
        return "y = " + a + "e^{" +b + "t} * cos(" + c + "t + " + d + ") + " + h + " \left\{t >= " + str(this._lastpoints[0][0]) + "\\right\}"

    
    def showPlot(this, coefs=None, extendBy=0):
        if coefs == None:
            coefs = this._last

        a,b,c,d,h = coefs


        x = []
        y = []
        i = points[0][0]
        while i <  points[-1][0] + extendBy:
            x.append(i)
            y.append(this._getValue(a,b,c,d,h,i))
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


if "__main__" in __name__:
    """
    example regression, takes a set of points and calculates a ... h
    as well as plots with matplotlib and outputs desmos + readable equations
    """


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



    regr = ODE2Regr()

    print(regr.regress(points))

    print(regr.getEquation())
    print(regr.getDesmosEquation())
    regr.showPlot()
    

    #for p in regr._getLocalExtrema(points)[0]:
    #    print(points[p])

    

    ###PLOT###

    



