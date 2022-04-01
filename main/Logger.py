class Logger:
    """
    A File Logging object\n
    creates a new file or appends to an existing one
    File is blocked until logger object is deleted using del obj
    """
    def __init__(this, file):
        this.file = open(file, "a")

    def __del__(this):
        this.file.close()
    
    def log(this, text="") -> None:
        this.file.write(text)

    def logLine(this, text="") -> None:
        this.log("\n" + text)
    