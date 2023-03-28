import time
import sys
import math

toolbar_width = 40

class ProgressBar:
    def __init__(self):
        self.percentage = 0
        self.message = ""
        self.update(0, "")

    def finishMessage(self, message, status):

        if status:
            statusMessage = "[✓]"
        else:
            statusMessage = "[⨯]"

        message = f"{statusMessage} {message}"

        lineSize = toolbar_width + len("||") + len(" {0}% {1}".format(self.percentage, self.message))
        sys.stdout.write("\b" * lineSize) # return to start of line, after '['

        clearSpace = lineSize - len(message)

        print(f'{message}{" "*clearSpace}')

        self.update(self.percentage, self.message)

    def smoothUpdate(self, percentage, message):
        startingPercentage = self.percentage
        self.update(self.percentage, message)
        for i in range(percentage - startingPercentage):
            self.update(self.percentage + 1, message)

    def update(self, percentage, message):

        lineSize = toolbar_width + len("||") + len(" {0}% {1}".format(self.percentage, self.message))

        sys.stdout.write("\b" * lineSize) # return to start of line, after '['

        filledCells = math.floor(self.percentage / 100.0 * toolbar_width)
        newFilledCells = math.floor(percentage / 100.0 * toolbar_width)

        sys.stdout.write("│")
        for i in range(filledCells):
            sys.stdout.write("█")

        sys.stdout.flush()

        for i in range(newFilledCells - filledCells):
            time.sleep(0.1) # do real work here
            # update the bar
            sys.stdout.write("█")
            sys.stdout.flush()

        for i in range(toolbar_width - newFilledCells):
            sys.stdout.write(" ")

        sys.stdout.write("│ {0}% {1}".format(percentage, message)) # this ends the progress bar
        sys.stdout.write("\033[K")
        sys.stdout.flush()

        self.percentage = percentage
        self.message = message

    def draw(self):
        filledCells = math.floor(self.percentage / 100.0 * toolbar_width)
        emptyCells = toolbar_width - filledCells

        sys.stdout.write("│{0}{1}│".format(("█" * filledCells), (" " * emptyCells)))
        sys.stdout.flush()
