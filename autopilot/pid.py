import calculus as calc
import regression as regr

points = [
    [-6,-7],
    [-3,-5.5],
    [-2,-5],
    [-1,-3],
    [0,0],
]

dest = 10

pt = regr.regress(points, 1000)

print(pt)

et = calc.mult(pt,-1)
et[0] += dest

et
iet = calc.integral0_x(et)
det = calc.dervivative(et)

print(et)
print(iet)
print(det)