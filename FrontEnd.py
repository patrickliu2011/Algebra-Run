from turtle import *
import tkinter
from random import random
from math import *
import numpy as np
from Backend_NoGraphics import *

#data = np.loadtxt('map.csv',dtype = int,delimiter=',')
#
##following command changes a numpy ndarray into an ordinary list of lists 
#myMatrix = data.tolist()
#print(myMatrix, type(myMatrix))  #just to check

show = False

class Ball(RawTurtle):

    def __init__(self,cv,dx,dy):
        super().__init__(cv)
        self.penup()
        self.shape("soccerball.gif")
        self.dx = dx
        self.dy = dy
        self.onfloor = True
        self.position = 0

    def move(self):
        newx = self.xcor() + self.dx
        newy = self.ycor() + self.dy
        
        if newy < 0:
            newy = 0
            self.dy = 0
        
        if (newy == 0):
            self.onfloor = True
        else:
            self.dy -= accel

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
        
class Orb(RawTurtle):
    def __init__(self,cv,dx,x_init,y_init):
        super().__init__(cv)
        self.penup()
        self.shape("circle.gif")
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
        self.done = False
        self.position = 0
        global jumps
    
    def over(self):
        self.done = True

    def buildWindow(self):

        root = self.master
        root.title("Algebra Run!")
        cv = ScrolledCanvas(root,600,600,600,600)
        cv.pack(side = tkinter.LEFT)
        t = RawTurtle(cv)
        t.speed(0)

        screen = t.getscreen()
        screen.setworldcoordinates(screenMinX,screenMinY,screenMaxX,screenMaxY)
        t.ht()

        screen.tracer(0)
        screen.register_shape("soccerball.gif")
        screen.register_shape("triangle.gif")
        screen.register_shape("square.gif")
        screen.register_shape("circle.gif")
        
        dx = 0
        dy = 0
        ball = Ball(cv,dx,dy)
        
        spikeList = []
        
        for i in range(5):
            spike = Spike(cv,v_screen,length/6*(i+1),0)
            spikeList.append(spike)
            
        blockList = []
        
        for i in range(int(length/20)):
            block = Block(cv,v_screen,i*20,-20)
            blockList.append(block)
            
        orbList = []
        
        orbList.append(Orb(cv,v_screen,400,50))
            
        lastblock = Block(cv,v_screen,length,0)

        def winHandler():
            if (lastblock.xcor() < 13):
                self.over()
                print("You win!")
                global win
                win = True
                quitHandler();
        
        
        def deathHandler():
            global win
            for spike in spikeList:
                if (abs(spike.xcor()-ball.xcor()) < 20 and abs(spike.ycor()-ball.ycor()) < 20):
                    print("You died!")
                    win = False
                    quitHandler()
                    
            for block in blockList:
                if (abs(block.xcor()-ball.xcor()) < 20 and abs(block.ycor()-ball.ycor()) < 20):
                    print("You died!")
                    win = False
                    quitHandler()

        # Here is the animation handler. It is called at
        # every timer event.
        
        def animate():
    
            winHandler()
            deathHandler()
            ball.position -= v_screen
            jumpHandler()
            ball.move()
            for spike in spikeList:
                spike.move()
            for block in blockList:
                block.move()
            for orb in orbList:
                orb.move()
            lastblock.move()
            if show:
                screen.update()
            screen.ontimer(animate)
    
        # This is the code for the quit Button handling. This
        # function will be passed to the quitButton so it can
        # be called by the quitButton when it wasPressed.
        def quitHandler():
            # close the window and quit
            print("Game Over")
            global finalPosition
            finalPosition = ball.position
            root.destroy()
            root.quit()
    
        quitButton = tkinter.Button(self, text = "Quit", command=quitHandler)
        quitButton.pack()
        
        def jumpHandler():
            if (ball.position in jumps):
                if ball.onfloor:
                    ball.onfloor = False
                    ball.dy = v_jump;
                for orb in orbList:
                    if (abs(orb.xcor()-ball.xcor()) < 20 and abs(orb.ycor()-ball.ycor()) < 20):
                        ball.dy = v_jump
                    
 
        screen.ontimer(animate)


show = True
value = input("Enter anything to show the winning trial: ")
print("Here's the winning trial: ")
print(jumps)
root = tkinter.Tk()
jumpingBallApp = JumpingBallApplication(root)
jumpingBallApp.mainloop()
show = False

print("Program Execution Completed.")

