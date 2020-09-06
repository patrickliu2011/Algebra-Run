from turtle import *
import tkinter
from random import random
from math import *
import numpy as np
from LoadLevel import *
from time import sleep

#bounds of array (in pixels, relative to the ball)
#currently, creates a window from 100 pix below and to the left
#to 300 pix above and to the right of the ball
screenMaxX = 300
screenMaxY = 350
screenMinX = -100
screenMinY = -50

#speed at which the map moves
#currently set at 5 pix/frame
#for reference, each square on the map is 20 pix
#negative is to the left
v_screen = -5

#speed at which the ball jumps vertically (in pix/frame)
#upward is positive
v_jump = 10

#acceleration of ball in midair (in pix/frame^2)
#positive is downward
accel = 1

#loads the level
list_blocks,list_spikes,list_orbs,length = getLevel()

win = False             #whether a trial has won

jumps = []              #the list of locations for jumps

#This class is the object for the ball (the player), including how to 
#initialize it and how to move it on the screen
class Ball(RawTurtle):

    #initializes the ball at an input position (pix) on the screen
    #and speed (pix/frame). For the code to work correctly, dx should be 0
    def __init__(self,cv,dx,dy):
        super().__init__(cv)
        self.penup()
        self.shape("soccerball.gif")
        self.goto(0,0)           #places ball's turtle at input coordinates
        self.dx = dx             #x-velocity (pix/frame), should be 0
        self.dy = dy             #y-velocity (pix/frame)
        self.onfloor = True      #stores whether the ball is on a block
        self.position = 0        #stores how far the ball has traveled

    #updates the ball's position based off of its velocity,
    #and changes its y-velocity based on acceleration
    def move(self):
        newx = self.xcor() + self.dx
        newy = self.ycor() + self.dy
       
       #makes sure ball doesnt go into floor 
        if self.onfloor:
            self.dy = 0
        else:
            self.dy -= accel

        self.goto(newx,newy)

#These objects encode the spikes, blocks, and orbs.
class Spike(RawTurtle):
    #initializes object at input coordinates and x-velocity (should be v_screen)
    #y-velocity will be 0
    def __init__(self,cv,dx,x_init,y_init,shape):
        super().__init__(cv)
        self.penup()
        self.shape(shape)
        self.dx = dx
        self.x_init = x_init
        self.y_init = y_init
        self.goto(x_init,y_init)

    #moves (to the left) without acceleration
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

#This class will run the actual game.
class JumpingBallApplication(tkinter.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.pack(side = tkinter.RIGHT,fill=tkinter.BOTH)
        self.buildWindow()      #begins the program
        self.done = False       #true if has won/died
        self.position = 0       #x-distance of ball
        global jumps

    #marks the class as done
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

        ball = Ball(cv,0,0)
        
        #stores list of Block objects
        blockList = []
        
        for coord in list_blocks:
            block = Block(cv,v_screen,coord[0],coord[1])
            blockList.append(block)
        
        #stores list of Spike objects
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
        
        #stores list of Orb objects    
        orbList = []
        
        for coord in list_orbs:
            orb = Orb(cv,v_screen,coord[0],coord[1])
            orbList.append(orb)
        
        #stores a final block which will be where the map ends    
        lastblock = Block(cv,v_screen,length,0)
        
        dotList = []

        #if the game has been won, quits the game
        def winHandler():
            if (lastblock.xcor() < 10):
                self.over()
                print("You win!")
                global win
                win = True
                quitHandler();
        
        #if the game has been lost, quits the game
        def deathHandler():
            global win
            #determines if ball has run into a spike
            for spike in spikeList:
                if (abs(spike.xcor()-ball.xcor()) < 15 and abs(spike.ycor()-ball.ycor()) < 15):
                    print("You died!")
                    win = False
                    quitHandler()
                    break
              
            #determines if ball has run into a block      
            for block in blockList:
                if (abs(block.xcor()-ball.xcor()) < 20 and abs(block.ycor()-ball.ycor()) < 20):
                    print("You died!")
                    win = False
                    quitHandler()
                    break

        #animates the actions recursively by moving the ball,
        #checking checking for win or death, then moving the
        #map.
        def animate():
            ball.position -= v_screen
            landHandler()
            jumpHandler()
            ball.move()
            dotList.append(Dot(cv,v_screen,0,ball.ycor()))
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
            screen.update()
            screen.ontimer(animate)
    
        #quits the program and sets finalPosition to the ball's last position
        def quitHandler():
            # close the window and quit
            print("Game Over")
            global finalPosition
            finalPosition = ball.position
            root.quit()
            root.destroy()
        
        #if the ball is not moving up and is close to a block, 
        #snaps ball location to top of block so that the ball 
        #doesn't go into the block. Then identifies the ball as
        #on the block (so that it can jump)
        def landHandler():
            ball.onfloor = False
            if (ball.dy <= 0):
                for block in blockList:
                    if abs(block.xcor()-ball.xcor()) < 20:
                        dely = ball.ycor()-block.ycor()
                        if dely <= 20 - ball.dy and dely >= 20:
                            ball.dy = block.ycor()-ball.ycor()+20
                            ball.onfloor = True
                            #print("on the floor at",ball.position)
                            break
                            
        #If the ball is supposed to jump and can jump (is on top 
        #of a block or on an orb), then jumps by setting y-velocity
        #to v_jump. Then marks ball as not on floor if jumped off 
        #of a block.        
        def jumpHandler():
            if (ball.position in jumps):
                if ball.onfloor:
                    ball.onfloor = False
                    ball.dy = v_jump;
                for orb in orbList:
                    if (abs(orb.xcor()-ball.xcor()) < 20 \
                        and abs(orb.ycor()-ball.ycor()) < 20):
                        ball.dy = v_jump
                        ball.onfloor = False
                        break
                    
        #pauses the game for 20s if the button is pressed
        def pauseHandler():
            sleep(20)    
        pauseButton = tkinter.Button(self, text = "Pause (20s)", command=pauseHandler)
        pauseButton.pack()
        
        #initializes the animation loop
        screen.ontimer(animate)
