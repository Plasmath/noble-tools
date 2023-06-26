import matplotlib.pyplot as plt
import matplotlib.colors as col
import numpy as np
from coordinates import tetrahedral, octahedral, kioctahedral, pyritohedral, icosahedral,
from volumes import minvol

"""Specifications for plotting"""
symmetry = octahedral #Symmetry used
startpoint = (1,1) #Plot starting point (bottom left corner)
endpoint = (4,4) #Plot ending point (top right corner)
resolution = 10 #Number of measurements per side

maxval = 8 #Volume cap, any higher value will be set to this one on the plot

def main():
    #remove first and last values because endpoints tend to act weirdly
    yaxis = list(np.linspace(startpoint[0],endpoint[0],num=resolution))[1:-1]
    xaxis = list(np.linspace(startpoint[1],endpoint[1],num=resolution))[1:-1]
    
    xvalues, yvalues = np.meshgrid(xaxis,yaxis)
    
    armyvols = [[minvol(symmetry(xvalues[j][i],yvalues[j][i]), maxval) for i in range(resolution - 2)] for j in range(resolution - 2)]
    
    print("Plotting!")
    ma = max([max(l) for l in armyvols])
    mi = min([min(l) for l in armyvols])
    
    fig, ax = plt.subplots(figsize=(10, 10))
    plt.imshow(armyvols, cmap='plasma', norm=col.LogNorm(vmin=mi, vmax=ma), extent=[startpoint[0],endpoint[0],startpoint[1],endpoint[1]])
    plt.legend()
    plt.savefig('filename.png',dpi=300)
    
if __name__ == "__main__":
    main()