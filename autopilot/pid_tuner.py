def restrict(var, min, max):
    """restricts a variable with provide min and max"""
    if var < min:
        return min
    if var > max:
        return max
    return var

def sum(ls):
    """adds all components of a given list"""
    out = 0
    for val in ls:
        out += val
    return out

def pid(Kp, Ki, Kd, print_values = False):
    prev = {
        "derivative": None,
        "integral": [],
    }

    heading = start_heading
    time = 0

    if print_values:
        print("(0, " + str(heading) + ")")

    while True:
        error = desired_heading - heading

        derivative_term = error
        if prev["derivative"] != None:
            derivative_term -= prev["derivative"]   
        derivative_term *= -1

        val_p = Kp * error
        val_i = Ki * sum(prev["integral"])
        val_d = Kd * derivative_term

        prev["derivative"] = error
        prev["integral"].append(error)

        if len(prev["integral"]) == 6:
            prev["integral"] = prev["integral"][1::]


        mid_servo_range = (max_servo_range-min_servo_range)/2.0

        adjustment = val_p + val_i + val_d
        left = mid_servo_range + adjustment
        right = mid_servo_range - adjustment

        left = restrict(left, min_servo_range, max_servo_range)
        right = restrict(right, min_servo_range, max_servo_range)

        
        dir = -1
        if (left-mid_servo_range) > 0:
            dir = 1
        heading = heading + ((left-mid_servo_range)/50)**3
        
        time += 1
        
        if print_values:
            print("(" + str(time) + ", " + str(heading) + ")")


        reachedZero = True
        for val in prev["integral"]:
            if (abs(val) > 0.005):
                reachedZero = False
        if time < 5:
            reachedZero = False


        if reachedZero or time > 1000:
            return time

def getNumPlaces(precision):
    p = 1/precision
    places = 0
    while p > 1:
        p = p/10
        places += 1
    return places

#first pass should be [0,0,0], 1, [-5,5]
def tuningpass(offset, precision, set):
    min_time = None
    values = []
    for p in range(set[0],set[1]):
        for i in range(set[0],set[1]):
            for d in range(set[0],set[1]):
                places = getNumPlaces(precision)
                Kp = round(p*float(precision) + offset[0], places)
                Ki = round(i*float(precision) + offset[1], places)
                Kd = round(d*float(precision) + offset[2], places)
                t = pid(Kp,Ki,Kd)
                if min_time == None or t < min_time:
                    #print(t, Kp/10.0,Ki/10.0,Kd/10.0)
                    min_time = t
                    values = [Kp, Ki, Kd]
    return values


desired_heading = 0 #degrees
start_heading = 60
max_servo_range = 270
min_servo_range = 0


if "__main__" in __name__:
    last = []
    while True:
        choice = input("min, test, last: ")

        if choice == "min":
            start_heading = float(input("start heading: "))
            
            values = [0,0,0]
            precision = 0.1
            set = [-10,10]

            for i in range(4): #4 passes
                values = tuningpass(values, precision, set)
                precision /= 10
            
            
            pid(values[0], values[1], values[2], True)
            print(values)
            last = values

        elif choice == "test":
            Kp = float(input("Kp: "))
            Ki = float(input("Ki: "))
            Kd = float(input("Kd: "))
            start_heading = float(input("start heading: "))
            pid(Kp, Ki, Kd, True)
        elif choice == "last" and len(last) > 1:
            start_heading = float(input("start heading: "))
            pid(last[0],last[1],last[2],True)