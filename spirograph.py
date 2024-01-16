"""
    Title: Spirograph.py

    Description: This is a program that brings up the turtle GUI, and draws four spirographs at the same time.
               The spirographs are completely random, meaning everytime you run the program, you get something 
               different each time. You can show the turtles by clicking "T" and reset the spirographs by clicking 
               the "space" key.
    
        Developer: Esad Mrkulic
"""

import math
import turtle
import random
from datetime import datetime
from PIL import Image
import argparse


class Spiro:
    # constructor
    def __init__(self, xc, yc, col, R, r, l):
        # Create the Turtle object
        self.t = turtle.Turtle()

        # Set the cursor shape
        self.t.shape("turtle")

        # Set the step in degrees
        self.step = 5

        # Set the drawing complete flag
        self.drawingComplete = False

        # Set the parameters
        self.setparams(xc, yc, col, R, r, l)

        # Initialize the drawing
        self.restart()

    # Set the parameters
    def setparams(self, xc, yc, col, R, r, l):
        # The Spirograph parameters
        self.xc = xc
        self.yc = yc
        self.R = int(R)
        self.r = int(r)
        self.l = l
        self.col = col

        # Reduce r/R to its smallest form by dividing with GCD (Greatest Common Diviser)
        gcdVal = math.gcd(self.r, self.R)
        self.nRot = self.r // gcdVal

        # Get ratio of radii
        self.k = r / float(R)

        # Set the color
        self.t.color(*col)

        # Store the current angle
        self.a = 0

    def restart(self):
        # Set the flag
        self.drawingComplete = False

        # Show the turtle
        self.t.showturtle()

        # Go to first pont
        self.t.up()
        R, k, l = self.R, self.k, self.l
        a = 0.0
        x = R * ((1 - k) * math.cos(a) + l * k * math.cos((1 - k) * a / k))
        y = R * ((1 - k) * math.sin(a) - l * k * math.sin((1 - k) * a / k))
        try:
            self.t.setpos(self.xc + x, self.yc + y)
        except:
            print("Exception, exiting.")
            exit(0)
        self.t.down()

    def draw(self):
        # Draw the rest of the points
        R, k, l = self.R, self.k, self.l
        for i in range(0, 360 * self.nRot + 1, self.step):
            a = math.radians(i)
            x = R * ((1 - k) * math.cos(a) + l * k * math.cos((1 - k) * a / k))
            y = R * ((1 - k) * math.sin(a) - l * k * math.sin((1 - k) * a / k))

            try:
                self.t.setpos(self.xc + x, self.yc + y)
            except:
                print("Exception, exiting.")
                exit(0)

            # Drawing is now done so hide the turtle cursor
        self.t.hideturtle()

    def update(self):
        # Skip the rest of the steps if done
        if self.drawingComplete:
            return
        # Increment the angle
        self.a += self.step

        # Draw a step
        R, k, l = self.R, self.k, self.l

        # Set the angle
        a = math.radians(self.a)
        x = R * ((1 - k) * math.cos(a) + l * k * math.cos((1 - k) * a / k))
        y = R * ((1 - k) * math.sin(a) - l * k * math.sin((1 - k) * a / k))

        try:
            self.t.setpos(self.xc + x, self.yc + y)
        except:
            print("Exception, exiting.")
            exit(0)

        # If drawing is complete, then set the flag
        if self.a >= 360 * self.nRot:
            self.drawingComplete = True

            # Drawing is now done so hide the turtle cursor
            self.t.hideturtle()

    # Clear everything
    def clear(self):
        # Pen up
        self.t.up()

        # Clear turtle
        self.t.clear()


# The class for animating the spiros
class SpiroAnimator:
    # Constructor
    def __init__(self, N):
        # Set the timer value in milliseconds
        self.deltaT = 10

        # Get the window dimensions
        self.width = turtle.window_width()
        self.height = turtle.window_height()

        # Restarting
        self.restarting = False

        # Create the Spiro objects
        self.spiros = []
        for i in range(N):
            # Generate random parameters
            rparams = self.genRandomParams()

            # Set the Spiro parameters
            spiro = Spiro(*rparams)
            self.spiros.append(spiro)
        # Call timer
        turtle.ontimer(self.update, self.deltaT)

    def restart(self):
        # Ignore restart if already in the middle of restarting
        if self.restarting:
            return
        else:
            self.restarting = True

        for spiro in self.spiros:
            # Clear
            spiro.clear()

            # Generate random parameters
            rparams = self.genRandomParams()

            # Set the spiro parameters
            spiro.setparams(*rparams)

            # Restart drawing
            spiro.restart()

        # Done restarting
        self.restarting = False

    # Generate random parameters for the spirographs
    def genRandomParams(self):
        width, height = self.width, self.height
        R = random.randint(50, min(width, height) // 2)
        r = random.randint(10, 9 * R // 10)
        l = random.uniform(0.1, 0.9)
        xc = random.randint(-width // 2, width // 2)
        yc = random.randint(-height // 2, height // 2)
        col = (random.random(), random.random(), random.random())
        return (xc, yc, col, R, r, l)

    def update(self):
        # Update all spiros
        nComplete = 0
        for spiro in self.spiros:
            # Update
            spiro.update()
            # Count completed spiros
            if spiro.drawingComplete:
                nComplete += 1
        # Restart if all spiros are complete
        if nComplete == len(self.spiros):
            self.restart()
        # Call the timer
        try:
            turtle.ontimer(self.update, self.deltaT)
        except:
            print("Exception, exiting.")
            exit(0)

    # Toggling the turtle in program with "T" key
    def toggleTurtles(self):
        for spiro in self.spiros:
            if spiro.t.isvisible():
                spiro.t.hideturtle()
            else:
                spiro.t.showturtle()


def saveDrawing():
    # Hide the turtle cursor
    turtle.hideturtle()

    # Generate unique filenames
    dateStr = (datetime.now()).strftime("%d%b%Y-%H%M%S")
    file_name = "spiro-" + dateStr
    print("Saving drawing to {}.eps/png".format(file_name))

    # Get the tkinter canvas
    canvas = turtle.getcanvas()

    # Save the drawing as a postscript image
    canvas.postscript(file=file_name + ".eps")

    # Use the Pillow module to convert the postscript image file to PNG
    img = Image.open(file_name + ".eps")
    img.save(file_name + ".png", "png")

    # Show the turtle cursor
    turtle.showturtle()


def main():
    # Use sys.argv if needed
    print("Generating Spirograph...")
    descStr = """This program draws a spirograph using Turtle. When it is run with no arguments, the program draws random spirographs.

    Terminology:
    
    R: radius of outer circle
    r: radius of inner circle
    l: ratio of hole distance to r
    """

    parser = argparse.ArgumentParser(description=descStr)

    # Add expected arguments
    parser.add_argument(
        "--sparams",
        nargs=3,
        dest="sparams",
        required=False,
        help="The three arguments in sparams: R, r, l.",
    )

    # Parse args
    args = parser.parse_args()

    # Set the width of the drawing window to 80 percent of the screen width
    turtle.setup(width=0.8)

    # Set the cursor shape to turtle
    turtle.shape("turtle")

    # Set the title to Spirographs!
    turtle.title("Spirographs!")

    # Add the key handler to save our drawings
    turtle.onkey(saveDrawing, "s")

    # Start listening
    turtle.listen()

    # Hide the main turtle cursor
    turtle.hideturtle()

    # Check for any arguments sent to --sparams and draw the Spiro
    if args.sparams:
        params = [float(x) for x in args.sparams]
        # Draw the Spiro with the given parameters
        col = (0.0, 0.0, 0.0)
        spiro = Spiro(0, 0, col, *params)
        spiro.draw()
    else:
        # Create the animator abject
        spiroAnim = SpiroAnimator(4)

        # Add a key handler to toggle the turtle cursor
        turtle.onkey(spiroAnim.toggleTurtles, "t")

        # Add a key handler to restart the animation
        turtle.onkey(spiroAnim.restart, "space")

    # Start the turtle main loop
    turtle.mainloop()


if __name__ == "__main__":
    main()
