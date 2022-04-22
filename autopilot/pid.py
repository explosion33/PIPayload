class PID:
    def __init__(this, Kp, Ki, Kd, setpoint):
        this.Kp = Kp
        this.Ki = Ki
        this.Kd = Kd
    
        this.lastErrors = []
        this.maxErrors = 5

        this.min = None
        this.max = None

        this.setpoint = setpoint
    

    def sumErrors(this) -> float:
        sum = 0
        for val in this.lastErrors:
            sum += val
        return sum

    def getErrorChange(this):
        l = len(this.lastErrors)
        if l < 2:
            return 0

        return (this.lastErrors[l-1] - this.lastErrors[l-2])
        


    def getControlVariable(this, ProcessVariable):
        error = this.setpoint - ProcessVariable # current error

        # add error to list of previous errors
        # if there are too many stored errors, removed oldest one
        this.lastErrors.append(error)
        if len(this.lastErrors) > this.maxErrors:
            this.lastErrors = this.lastErrors[1::]

        # calculate control variable, and constrain
        p = error                 * this.Kp
        i = this.sumErrors()      * this.Ki
        d = this.getErrorChange() * this.Kd

        u = p + i + d

        if this.min != None and u < this.min:
            u = this.min
        if this.max != None and u > this.max:
            u = this.max
        return u


    def changeSetPoint(this, setpoint):
        """reset controlller with a new setpoint"""
        this.lastErrors = []
        this.setpoint = setpoint



if "__main__" == __name__:
    sp = float(input("Enter Desired Heading: "))
    headingController = PID(6.9, 2.0, -4.89, sp)
    headingController.min = -135
    headingController.max = 135

    points = []

    while True:
        pv = float(input("Enter Current Heading: "))
        if (pv > 360): break

        c = headingController.getControlVariable(pv)
        print(c,((c/135)**3)*30/10)
        points.append(pv)

    t  = 0
    for y in points:
        print("(", t, ",", y, ")")
        t += 1
    
