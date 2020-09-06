from turtle import *
import tkinter
from random import random
from math import *
import numpy as np
from LoadLevel import *
from time import sleep

screenMaxX = 300
screenMaxY = 350
screenMinX = -100
screenMinY = -50

v_screen = -5

v_jump = 10
accel = 1

length = 0

win = False

#data = np.loadtxt('map.csv',dtype = int,delimiter=',')
#
##following command changes a numpy ndarray into an ordinary list of lists 
#myMatrix = data.tolist()
#print(myMatrix, type(myMatrix))  #just to check

show = False

list_blocks,list_spikes,list_orbs,length = getLevel()

class Ball(RawTurtle):

    def __init__(self,cv,dx,dy):
        super().__init__(cv)
        self.penup()
        self.shape("soccerball.gif")
        self.goto(0,0)
        self.dx = dx
        self.dy = dy
        self.onfloor = True
        self.position = 0

    def move(self):
        newx = self.xcor() + self.dx
        newy = self.ycor() + self.dy
        
        if self.onfloor:
            self.dy = 0
        else:
            self.dy -= accel

        self.goto(newx,newy)

class Spike(RawTurtle):
    
    def __init__(self,cv,dx,x_init,y_init,shape):
        super().__init__(cv)
        self.penup()
        self.shape(shape)
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

class Dot(RawTurtle):
    def __init__(self,cv,dx,x_init,y_init):
        super().__init__(cv)
        self.penup()
        self.shape("dot.gif")
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
        screen.register_shape("triangle_inv.gif")
        screen.register_shape("square.gif")
        screen.register_shape("circle.gif")
        screen.register_shape("dot.gif")

        ball = Ball(cv,v_screen,0)
        
        blockList = []
        
        for coord in list_blocks:
            block = Block(cv,v_screen,coord[0],coord[1])
            blockList.append(block)
        
        spikeList = []
        
        for coord in list_spikes:
            inv = True
            for block_coord in list_blocks:
                if coord[0] == block_coord[0] and coord[1] == block_coord[1]+20:
                    inv = False
                    break
            shape = "triangle.gif"
            if inv:
                shape = "triangle_inv.gif"
            spike = Spike(cv,v_screen,coord[0],coord[1],shape)
            spikeList.append(spike)
            
        orbList = []
        
        for coord in list_orbs:
            orb = Orb(cv,v_screen,coord[0],coord[1])
            orbList.append(orb)
            
        lastblock = Block(cv,v_screen,length,0)
        
        dotList = []

        def winHandler():
            if (lastblock.xcor() < 10):
                self.over()
                print("You win!")
                global win
                win = True
                quitHandler();
        
        
        def deathHandler():
            global win
            for spike in spikeList:
                if (abs(spike.xcor()-ball.xcor()) < 15 and abs(spike.ycor()-ball.ycor()) < 15):
                    print("You died!")
                    print("ball was at:",ball.xcor(),ball.ycor())
                    print("spike was at:",spike.xcor(),spike.ycor())
                    win = False
                    quitHandler()
                    break
                    
            for block in blockList:
                if (abs(block.xcor()-ball.xcor()) < 20 and abs(block.ycor()-ball.ycor()) < 20):
                    print("You died!")
                    print("ball was at:",ball.xcor(),ball.ycor())
                    print("block was at:",block.xcor(),block.ycor())
                    win = False
                    quitHandler()
                    break

        # Here is the animation handler. It is called at
        # every timer event.
        
        def animate():
            ball.position -= v_screen
            landHandler()
            jumpHandler()
            ball.move()
            #dotList.append(Dot(cv,v_screen,0,ball.ycor()))
            winHandler()
            if not win:
                deathHandler()
            for spike in spikeList:
                spike.move()
            for block in blockList:
                block.move()
            for orb in orbList:
                orb.move()
            for dot in dotList:
                dot.move()
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
            root.quit()
        
        def landHandler():
            ball.onfloor = False
            if (ball.dy <= 0):
                for block in blockList:
                    if abs(block.xcor()-ball.xcor()) < 20:
                        dely = ball.ycor()-block.ycor()
                        if dely <= 20 - ball.dy and dely >= 20:
                            ball.dy = block.ycor()-ball.ycor()+20
                            ball.onfloor = True
                            break
        
        def jumpHandler():
            if (ball.position in jumps):
                if ball.onfloor:
                    ball.onfloor = False
                    ball.dy = v_jump;
                for orb in orbList:
                    if (abs(orb.xcor()-ball.xcor()) < 20 and abs(orb.ycor()-ball.ycor()) < 20):
                        ball.dy = v_jump
                        ball.onfloor = False
                        break
        
        def pauseHandler():
            sleep(20)
            
        pauseButton = tkinter.Button(self, text = "Pause (20s)", command=pauseHandler)
        pauseButton.pack()
 
        screen.ontimer(animate)

jumps = []

show = True
value = input("Enter anything to show the map: ")
root = tkinter.Tk()
jumpingBallApp = JumpingBallApplication(root)
jumpingBallApp.mainloop()
show = False

print("Program Execution Completed.")