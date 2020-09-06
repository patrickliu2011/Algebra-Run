# Algebra-Run

## Run Instructions
To run from terminal, use the command 
'''
python3 Front.py
'''

Backend_NoGraphics.py runs training until the program wins, and outputs the results of each generation

Front.py  runs Backend_NoGraphics.py and displays with graphics

Graphics.py runs a game with a hardcoded list of places to jump. The last definition of the variable 'jumps' is the list of jumps that will be run

LoadLevels.py retrieves the level from csv (currently set to 'level2.csv')
.gif's are the images 

show_dots in Front.py determines if dots are shown

kept in Backend_NoGraphics.py determines how many trials are kept per generation

the jumps = [...] at the top of Backend_NoGraphics.py should be blank for a normal run, but can be seeded as the base case of locations to jump to start with
