"""
considetations

how can we account for angle travel speed?
    time degree/s of servo, adjust function to run at this rate?
"""


from PID import PID
from multiprocessing import Process, Queue

def transfer(x):
    """
    how does the output of the PID relate to change in PV
    i.e., how does the angle offset of the wings relate to the change in heading

    currently
    y = 30(x/135)^3 {-135 <= x <= 135}
        corresponds to a non-linear curve with max speed 30 degrees/s
    using 30/10 to run in degrees / (1/10s)
    """
    if x > 135:
        x = 135
    if x < -135:
        x = -135
    # y=30(x/135)^3 {-135 <= x <= 135}

    return 30/10*(x/135)**3


def execute_pid(kP, kI, kD, sp=0, start=60, maxError=0.05, maxCycles=200, debug=False):
    """
    execute_pid() | creates and executes a pid controller until it reaches
    and stays at zero or reaches a maximun number of cyckes

    kP            | (float)
    kI            | (float)
    kD            | (float)
    sp            | (float) desired setpoint
    start         | (float) (default=60) starting PV
    maxError      | (float) (default=0.05) maximum error until we can say PV = SP
    maxCycles     | (float) (default=200) maximum number of iterations before exiting
    returns number of cycles to reach 0, or maxCycles
    """

    # initiate controller, currently setup for heading/elevon example
    controller = PID(kP, kI, kD, sp)
    controller.min = -135
    controller.max = 135

    currHeading = start
    cycles = 0
    lastErrs = []
    while True:
        offset = controller.getControlVariable(currHeading)

        if debug:
            print(cycles, currHeading, offset, transfer(offset))
       
        currHeading += transfer(offset)
        cycles += 1

        if cycles >= maxCycles:
            break

        # add current error to a list of errors, maintain this list at len 5
        error = abs(currHeading - sp)
        lastErrs.append(error)
        if len(lastErrs) > 5:
            lastErrs = lastErrs[1::]
        
        # if all current errors are under the maximum error, exit and return
        allLess = True
        for error in lastErrs:
            if error > maxError:
                allLess = False
        if len(lastErrs) == 5 and allLess:
            break

    return cycles

def getNumPlaces(x):
    """
    getNumPlaces() | gets the number of decimal places in a float/integer
    x | (float) (int)
    returns (int)
    """
    if int(x) == x:
        return 0
    return len(str(x)) - len(str(int(x))) - 1

def rangeF(start,stop,step):
    """
    rangeF() | creates a list of numbers from start to stop by step
    start | (float) inclusive
    stop  | (float) exclusive
    step  | (float)
    returns (list( (float) ))
    """
    numplaces = getNumPlaces(step)
    l = []
    while True:
        l.append(start)
        start += step
        start = round(start,numplaces)
        if start >= stop:
            return l


def getMaxPerKPs(kPs, rangeI, rangeD, queue, sp=0, start=60, maxError=0.05, maxCycles=200):
    """
    getMaxPerKPs() | utility function for running through a range of PID coeffecients
    inside of a process, and getting the set of coefficients that produces the minimum
    number of cycles

    kPs            | (list( (float) )) list of all kP to check
    kIs            | (list( (float) )) list of all kI to check
    kDs            | (list( (float) )) list of all kD to check
    queue          | (multiprocessing.Queue)
    sp             | (float) desired setpoint
    start          | (float) (default=60) starting PV
    maxError       | (float) (default=0.05) maximum error until we can say PV = SP
    maxCycles      | (float) (default=200) maximum number of iterations before exiting

    returns None,
    adds (numCycles, (kP,kI,kD)) to provided queue
    """
    max = (None,None)
    for kP in kPs:
        for kI in rangeI:
            for kD in rangeD:            
                c = execute_pid(kP,kI,kD, sp, start, maxError, maxCycles)
                if max[0] == None or c < max[0]:
                    max = (c, (kP,kI,kD))
    queue.put(max)



def main():
    GROUP_SIZE = 3 # how big of kP groups to make per process
    DECIMAL_PRECISION = 3 # how precise the final coeffecients should be

    # get initial values
    pRange = rangeF(-15,15,1)
    iRange = rangeF(-15,15,1)
    dRange = rangeF(-15,15,1)

    for i in range(DECIMAL_PRECISION+1):
        pcs = []
        for p in range(0,len(pRange),GROUP_SIZE):
            # create kP group of specified size
            # create queue and process and add to pcs
            l = [pRange[p+i] for i in range(GROUP_SIZE) if p+i < len(pRange)]
            q = Queue()
            p = Process(target=getMaxPerKPs, args=[l, iRange, dRange, q], kwargs={"start": 30, "maxCycles": 200})
            pcs.append((p,q))
        
            p.start()
        
        print("iteration", i+1, "/", DECIMAL_PRECISION+1)

        # wait for each process to finish, get its best rated coefficient set, and find
        # best out of all recieved sets
        max = None
        for pc in pcs:
            pc[0].join()
            res = pc[1].get()
            if max == None or res[0] < max[0]:
                max = res

        # get new range of coeffiencents
        # take each coefficeint and get +- 1 (of whatever decimal place we are at)
        # with a precision of 1/10 the previous precision
        coefs = max[1]
        pRange = rangeF(coefs[0]-1/(10**(i-1)), coefs[0]+1/(10**(i-1)), 1/(10**i))
        iRange = rangeF(coefs[1]-1/(10**(i-1)), coefs[1]+1/(10**(i-1)), 1/(10**i))
        dRange = rangeF(coefs[2]-1/(10**(i-1)), coefs[2]+1/(10**(i-1)), 1/(10**i))
        print(max)

    coefs = max[1]
    execute_pid(coefs[0],coefs[1],coefs[2], start=30, debug=True)


if "__main__" == __name__:
    main()

