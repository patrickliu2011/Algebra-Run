from turtle import *
import tkinter
import random
from math import *

screenMaxX = 300
screenMaxY = 300
screenMinX = -300
screenMinY = -300


#Finds angle in radians given sine and cosine of angle
def arctrig (sine, cosine):
    #checks that inputs are valid values of sine and cosine, or close enough
    if (abs(sine**2 + cosine**2 - 1) >= 0.001):
        return ('The inputs are not valid')
    elif (sine >= 0):                   #valid for 1st and 2nd quadrants
        return (acos (cosine))
    elif (sine < 0 and cosine >= 0):    #valid for 4th quadrant
        return (2*pi + asin (sine))
    elif (sine < 0 and cosine < 0):     #valid for 3rd quadrant
        return (2*pi - acos (cosine))
    else:                               #just in case
        return ('Something went wrong, check the code')

# This is a example of a class that uses inheritance.
# The Ball class inherits from the RawTurtle class.
# This is indicated to Python by writing
# class Ball(RawTurtle):
# That says, class Ball inherits from RawTurtle, which
# means that a Ball is also a RawTurtle, but it is a
# little more than just a RawTurtle. The Ball class also
# maintains a dx and dy value that is the amount
# to move as it is animated.
class Ball(RawTurtle):
    # The __init__ is the CONSTRUCTOR. Its purpose is to
    # initialize the object by storing data in the object. Anytime
    # self.variable = value is written a value is being stored in
    # the object referred to by self. self always points to the
    # current object.
    def __init__(self,cv,dx,dy):
        # Because the Ball class inherits from the RawTurtle class
        # the Ball class constructor must call the RawTurtle class
        # constructor to initialize the RawTurtle part of the object.
        # The RawTurtle class is called the BASE class. The Ball class
        # is called the DERIVED class. The call to initialize the
        # base class part of the object is always the first thing
        # you do in the derived class's constructor.
        #RawTurtle.__init__(self,cv)
        super().__init__(cv)

        # Then the rest of the object can be initialized.
        self.penup()
        self.shape("soccerball.gif")
        self.dx = dx
        self.dy = dy

    # The move method is a mutator method. It changes the data
    # of the object by adding something to the Ball's x and y
    # position.
    def move(self):
        newx = self.xcor() + self.dx
        newy = self.ycor() + self.dy
        
        self.dy -= 0.5

        # The if statements below make the ball
        # bounce off the walls.
        if newx < screenMinX + 32:
            newx = screenMinX + 32
            self.dx = -0.9 * self.dx
        if newy < screenMinY + 32:
            newy = screenMinY + 32
            self.dy = -0.9 * self.dy
        if newx > screenMaxX - 32:
            newx = screenMaxX - 32
            self.dx = -0.9 * self.dx
        if newy > screenMaxY - 32:
            newy = screenMaxY - 32
            self.dy = -0.9 * self.dy

        # Then we call a method on the RawTurtle
        # to move to the new x and y position.
        self.goto(newx,newy)


def collided(ball1, ball2):
	if ball1 is ball2:
		return False
	else:
		return (ball1.xcor()-ball2.xcor())**2 + (ball1.ycor() - ball2.ycor())**2 <= 1024


class BouncingBallsApplication(tkinter.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.pack(side = tkinter.RIGHT,fill=tkinter.BOTH)
        self.buildWindow()
        self.collisions = False

    def buildWindow(self):

        # Once the classes and functions have been defined we'll put our
        # main function at the bottom of the file. Main isn't necessarily
        # written last. It's simply put at the bottom of the file. Main
        # is not a method. It is a plain function because it is not
        # defined inside any class.

        # Start by creating a RawTurtle object for the window.
        root = self.master
        root.title("Bouncing Balls!")
        cv = ScrolledCanvas(root,600,600,600,600)
        cv.pack(side = tkinter.LEFT)
        t = RawTurtle(cv)

        screen = t.getscreen()
        screen.setworldcoordinates(screenMinX,screenMinY,screenMaxX,screenMaxY)
        t.ht()
        # The next line tells Turtle Graphics to not display anything in the
        # second buffer while it is being drawn unless explicitly told to do
        # so by calling screen.update().
        screen.tracer(0)
        # You must register a shape before a turtle can use the shape.
        screen.register_shape("soccerball.gif")

        # The ballList is a list of all the ball objects. This
        # list is needed so the balls can be animated by the
        # program.
        ballList = []

        # Here is the animation handler. It is called at
        # every timer event.
        
        def animate():
            # Tell all the balls to move
            for ball in ballList:
                ball.move()
            deadPool = set()
            
            if self.collisions:
                for ball1 in ballList:
                    for ball2 in ballList:
                        if collided(ball1, ball2):
                        	#find angle between centers of balls
                        	delx = ball2.xcor() - ball1.xcor()
                        	dely = ball2.ycor() - ball1.ycor()
                        	sin_del = dely/sqrt(delx**2 + dely**2)
                        	cos_del = delx/sqrt(delx**2 + dely**2)
                        	ang_del = arctrig(sin_del, cos_del)
                        	
                        	#find angle of ball2's velocity relative to ball1
                        	delvx = ball2.dx - ball1.dx
                        	delvy = ball2.dy - ball1.dy
                        	delv = sqrt(delvx**2 + delvy**2)
                        	sin_delv = delvy/delv
                        	cos_delv = delvx/delv
                        	ang_delv = arctrig(sin_delv, cos_delv)
                        	
                        	#radian angle between relative velocity and relative position
                        	theta = pi - ang_delv + ang_del
                        	
                        	ball2.dx = ball1.dx + delv*sin(theta)*cos(ang_delv+theta+pi/2)
                        	ball2.dy = ball1.dy + delv*sin(theta)*sin(ang_delv+theta+pi/2)
                        	
                        	ball1.dx = ball1.dx + delv * cos(theta)*cos(ang_delv+theta+pi)
                        	ball1.dy = ball1.dy + delv * cos(theta)*sin(ang_delv+theta+pi)
    
            screen.update()
            screen.ontimer(animate)
    
            # This code creates 10 balls heading
            # in random directions
        for k in range(10):
            dx = random.random() * 20 - 10
            dy = random.random() * 20 - 10
            # Here is how a ball object is created. We
            # write ball = Ball(5,4)
            # to create an instance of the Ball class
            # and point the ball reference at that object.
            # That way we can refer to the object by writing
            # ball.
            ball = Ball(cv,dx,dy)
            # Each new ball is added to the Ball list so
            # it can be accessed by the animation handler.
            ballList.append(ball)
    
        # This is the code for the quit Button handling. This
        # function will be passed to the quitButton so it can
        # be called by the quitButton when it wasPressed.
        def quitHandler():
            # close the window and quit
            print("Good Bye")
            root.destroy()
            root.quit()
    
        # Here is where the quitButton is created. To create
        # an object we write
        # objectReference = Class(<Parameters to Constructor>)
        quitButton = tkinter.Button(self, text = "Quit", command=quitHandler)
        quitButton.pack()
    
        # This is another example of a method call. We've been doing
        # this all semester. It is an ontimer method call to the
        # TurtleScreen object referred to by screen.
       
        
        def addHandler():
            dx = random.random() * 20 - 10
            dy = random.random() * 20 - 10
            ball = Ball(cv,dx,dy)
            ballList.append(ball)            
            
        addButton = tkinter.Button(self, text = "Add Ball", command=addHandler)
        addButton.pack()
        
        def colHandler():
        	self.collisions = not self.collisions
        	print (self.collisions)
        	return self.collisions
        
        colButton = tkinter.Button(self, text = "Toggle Collisions", command=colHandler)
        colButton.pack()
    
        screen.ontimer(animate)

def main():
    # This creates the root window.
    root = tkinter.Tk()
    # And here we make an instance of the BouncingBallsApplication
    # inside the root window.
    bouncingBallsApp = BouncingBallsApplication(root)

    # This is the call to the infinite event processing loop. It will terminate
    # when the application window is closed.
    bouncingBallsApp.mainloop()
    print("Program Execution Completed.")

if __name__ == "__main__":
    main()
