import numpy as np

file = "level4.csv"

#Returns lists of block, spike, and orb coordinates, as well as length of 
#the map in pixels, based on an input csv file, where 1 denotes blocks, 
#2 denotes spikes, and 3 denotes orbs.
def getLevel():

    #loads data from file and stores the dimensions of the data
    #as a list [# of rows, # of columns]
    data = np.loadtxt(file,dtype = int,delimiter=',')
    dimensions = data.shape
    
    #numpy array into a list of lists 
    myMatrix = data.tolist()
    
    #scales up the grid to number of pixels per cell
    scale = 20
    
    #gets the length and height of the map
    length = scale*dimensions[1]
    height = scale*dimensions[0]
    
    #lists of [x-coord, y-coord] for blocks, spikes, and orbs, respectively
    list_blocks = []            
    list_spikes = []            
    list_orbs = []              
    
    #categorizes each data item as block, spike, or orb and appends
    #coordinates to the appropriate list
    for i in range(len(myMatrix)):
        for j in range(len(myMatrix[i])):
            num = myMatrix[i][j]
            coord = [j*scale,height - (i+2)*scale]
            if num == 1:
                list_blocks.append(coord)
            elif num == 2:
                list_spikes.append(coord)
            elif num == 3:
                list_orbs.append(coord)
        
    return list_blocks,list_spikes,list_orbs,length
