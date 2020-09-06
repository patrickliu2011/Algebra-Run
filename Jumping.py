from turtle import *
import tkinter
import random
from math import *

screenMaxX = 300
screenMaxY = 300
screenMinX = -100
screenMinY = -100

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

    def __init__(self,cv,dx,dy):
        super().__init__(cv)
        self.penup()
        self.shape("soccerball.gif")
        self.dx = dx
        self.dy = dy
        self.onfloor = True

    def move(self):
        newx = self.xcor() + self.dx
        newy = self.ycor() + self.dy
        
        if newy < 0:
            newy = 0
            self.dy = 0
        
        if (newy == 0):
            self.onfloor = True
        else:
            self.dy -= 0.8

        self.goto(newx,newy)

class Spike(RawTurtle):
    
    def __init__(self,cv,dx,x_init,y_init):
        super().__init__(cv)
        self.penup()
        self.shape("triangle.gif")
        self.dx = dx
        self.x_init = x_init
        self.y_init = y_init
        self.goto(x_init,y_init)

    def move(self):
        newx = self.xcor() + self.dx
        newy = self.ycor()

        self.goto(newx,newy)
        
class Block(RawTurtle):
    def __init__(self,cv,dx,x_init,y_init):
        super().__init__(cv)
        self.penup()
        self.shape("square.gif")
        self.dx = dx
        self.x_init = x_init
        self.y_init = y_init
        self.goto(x_init,y_init)
        
    def move(self):
        newx = self.xcor() + self.dx
        newy = self.ycor()

        self.goto(newx,newy)

class JumpingBallApplication(tkinter.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.pack(side = tkinter.RIGHT,fill=tkinter.BOTH)
        self.buildWindow()

    def buildWindow(self):

        root = self.master
        root.title("Bouncing Balls!")
        cv = ScrolledCanvas(root,600,600,600,600)
        cv.pack(side = tkinter.LEFT)
        t = RawTurtle(cv)

        screen = t.getscreen()
        screen.setworldcoordinates(screenMinX,screenMinY,screenMaxX,screenMaxY)
        t.ht()

        screen.tracer(0)
        screen.register_shape("soccerball.gif")
        screen.register_shape("triangle.gif")
        screen.register_shape("square.gif")
        
        dx = 0
        dy = 0
        ball = Ball(cv,dx,dy)
        
        v_screen = -5
        
        spikeList = []
        
        for i in range(5):
            spike = Spike(cv,v_screen,300*i+300,0)
            spikeList.append(spike)
            
        blockList = []
        
        for i in range(90):
            block = Block(cv,v_screen,20*i,-20)
            blockList.append(block)
            
        lastblock = Block(cv,v_screen,20*90,0)

        def winHandler():
            if (lastblock.xcor() < 13):
                print("You win!")
                root.quit();
        
        
        def deathHandler():
            for spike in spikeList:
                if (abs(spike.xcor()-ball.xcor()) < 20 and abs(spike.ycor()-ball.ycor()) < 20):
                    print("You died!")
                    quitHandler()
                    
            for block in blockList:
                if (abs(block.xcor()-ball.xcor()) < 20 and abs(block.ycor()-ball.ycor()) < 20):
                    print("You died!")
                    quitHandler()

        # Here is the animation handler. It is called at
        # every timer event.
        
        def animate():
            winHandler()
            deathHandler()
            ball.move()
            for spike in spikeList:
                spike.move()
            for block in blockList:
                block.move()
            lastblock.move()
            screen.update()
            screen.ontimer(animate)
    
        # This is the code for the quit Button handling. This
        # function will be passed to the quitButton so it can
        # be called by the quitButton when it wasPressed.
        def quitHandler():
            print(lastblock.xcor())
            # close the window and quit
            print("Game Over")
            #root.destroy()
            root.quit()
    
        quitButton = tkinter.Button(self, text = "Quit", command=quitHandler)
        quitButton.pack()
        
        def jumpHandler():
            if ball.onfloor:
                ball.onfloor = False
                if ball.dy == 0:
                    ball.dy = 10;
    
        jumpButton = tkinter.Button(self, text = "Jump", command=jumpHandler)
        jumpButton.pack()
 
        screen.ontimer(animate)

def main():
    # This creates the root window.
    root = tkinter.Tk()
    # And here we make an instance of the BouncingBallsApplication
    # inside the root window.
    jumpingBallApp = JumpingBallApplication(root)

    # This is the call to the infinite event processing loop. It will terminate
    # when the application window is closed.
    jumpingBallApp.mainloop()
    print("Program Execution Completed.")

if __name__ == "__main__":
    main()
