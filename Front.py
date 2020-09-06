#runs backend
import Backend_NoGraphics as bck

import Graphic_Classes as gc

#Displays winning trial from Backend using graphics
gc.jumps = bck.jumpsList[0][0]
root = gc.tkinter.Tk()
jumpingBallApp = gc.JumpingBallApplication(root)
jumpingBallApp.mainloop()

print("Program Execution Completed.")

