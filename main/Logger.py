"""
Ethan Armstrong
warmst@uw.edu
implements Logger class
"""
class Logger:
    """
    A file logging object to handle the opening and closing of a file across multiple objects
    """
    def __init__(this, file):
        """
        Logger(file) | creates a new Logger object\n
        file | filename and extension to log to
        """
        this.file = open(file, "a")

    def __del__(this):
        """
        closes the file on deletion of the logger object
        """
        this.file.close()
    
    def log(this, text="") -> None:
        """
        log(text) | logs the given text to the file\n
        test | (str) text to be logged
        """
        this.file.write(text)

    def logLine(this, text="") -> None:
        """
        logLine(text) | logs the given text to the file on a new line, mimicing pythons print() method\n
        text | (str) text to be logged
        """
        this.log("\n" + text)
    