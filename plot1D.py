#Plots critical points of nobles in 1D using matplotlib
#Also relies on numpy
import matplotlib.pyplot as plt
import numpy as np
from coordinates import tetrahedral, octahedral, icosahedral, mergepoints
from volumes import findvols

"""Specifications for plotting"""
symmetry = octahedral #Symmetry used
startpoint = (1,1) #Plot starting point
endpoint = (4,1) #Plot ending point
resolution = 100 #Number of data points to be plotted

maxval = 1 #Volume cap, any higher value will be set to this one on the plot

merge = True #whether or not to attempt to merge identical points

def main():
    #remove first and last values because endpoints tend to act weirdly
    values = list(np.linspace(startpoint,endpoint, num = resolution))[1:-1]
    armies = list(map(lambda x: symmetry(*x), values))
    
    if merge: #Merge identical points if specified
        armies = [mergepoints(a) for a in armies]
    
    armyvols = []
    for i in range(len(armies)):
        a = armies[i]
        armyvols.append(findvols(a,maxval))
        print("Processed",i+1,"out of",len(armies),"armies")
    
    #obtains the data for the plot. Each element in data contains one cubic
    transposed = np.transpose(np.array(armyvols, dtype="object"))
    data = set(tuple(i) for i in transposed if min(i) < maxval)
    
    print("Plotting...")
    plt.figure(figsize=(10, 5.4))
    for d in data:
        plt.plot(values,d,linewidth=0.3)
    plt.xlabel('Values') #only shows x values
    plt.ylabel('Distance')
    plt.legend()
    plt.savefig('filename.png',dpi=300)

if __name__ == "__main__":
    main()