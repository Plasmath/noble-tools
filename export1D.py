import numpy as np
import sympy as sp
from coordinates import ratet, tut, sirco, tic, toe, srid, tid, ti, doSymbolic
from volumes import symvol, maketets, combineplanes
from itertools import groupby

"""
Creates two files within the output file:
    - critical-planes.txt: faceting data containing critical planes
    - cubics.txt: the cubics in text form 
"""

"""Specifications for solving"""
army = tid #Symmetry used
extension = sp.sqrt(5) #Optional extension to factoring, use sp.sqrt(5) on icosahedral

#volume function
vol = lambda p1,p2,p3,p4 : sp.expand(symvol(p1,p2,p3,p4))

#Decomposes polynomial into polynomial factors
def factorize(poly):
    L = sp.factor_list(poly, extension = extension)[1] #list of factors, with multiplicity
    return [f[0] for f in L if not f[0].is_constant()] #remove multiplicity and constants because we don't care about them

def hastripleintersection(l1,l2): #detects whether the intersection of two cubics could actually form new nobles
    for s1 in l1:
        for s2 in l2:
            if not s1 <= s2 and not s2 <= s1:
                if len(s1.intersection(s2)) > 2:
                    return True
    return False

def mps(poly): #"make poly string": converts to WolframScript-readable format
    return str(poly).replace("**","^").replace("sqrt(5)","Sqrt[5]").replace(" ","")

def main():
    doSymbolic(True) #use sympy coordinates
    
    a = sp.Symbol("a")
    coords = army(a)
    
    print("Obtained",len(coords),"vertices.")
    
    tets = maketets(range(len(coords))) #Tetrahedra as indices in coords, used for critical plane calculation
    
    cubics = [] #format: each element is [cubic,critical plane]
    length = len(tets)
    print(length,"tets.")
    for i in range(len(tets)):
        if i % 5000 == 0:
            print("Finished computing",i,"tets out of",length)
        tet = tets[i]
        
        cubics.append([sp.expand(symvol(coords[tet[0]],coords[tet[1]],coords[tet[2]],coords[tet[3]])),[set(tet)]])
    print("Finished computing",length,"tets out of", length)
    
    print("Matching cubics...")
    sharedplanes = [] #Planes that will always have volume 0 no matter what
    cubicsmatched = [] #Duplicate cubics are matched together
    for c in cubics:
        if c[0] == 0: #0 can't be factored
            sharedplanes = combineplanes(sharedplanes, c[1])
            continue
        
        newcubic = True
        for c1 in cubicsmatched:
            #Check if first and second cubic are the same cubic
            if c1[0] == c[0]:
                newcubic = False
                c1[1] = combineplanes(c1[1],c[1]) #Add second cubic's plane to this cubic
        if newcubic: #Adding new cubics to the list
            cubicsmatched.append(c)
    
    print("Factoring cubics...")
    cubicsfactored = [] #Separate cubics into their component factors
    for c in cubicsmatched:
        
        fl = [ [factor,c[1]] for factor in factorize(c[0]) ]
        cubicsfactored += fl
    cubicsfactored = [k for k,v in groupby(sorted(cubicsfactored, key=repr))]
    
    print("Final round of matching...")
    cubicsfinal = [] #Factored cubics are matched together
    for c in cubicsfactored:
        newcubic = True
        for c1 in cubicsfinal:
            #Check if first and second cubic are the same cubic
            if c1[0] == c[0]:
                newcubic = False
                c1[1] = combineplanes(c1[1],c[1]) #Add second cubic's plane to this cubic
        if newcubic: #Adding new cubics to the list
            cubicsfinal.append(c)
    
    #Files to be written to
    fcubics = open("output/cubics.txt","w")
    fplanes = open("output/critical-planes.txt","w")
    
    #Finding intersections
    fplanes.write("shared: " + str(sharedplanes) + "\n") #sharedplanes was made back in the first matching stage
    for i in range(0,len(cubicsfinal)):
        
        fcubics.write(str(i) + ": " + mps(cubicsfinal[i][0]) + "\n") #add cubic
        fplanes.write(str(i) + ": " + str(cubicsfinal[i][1]).replace(" ","")+"\n") #add data
        
        if i % 10 == 9:
            print("Finished cubic type",str(i+1)+"/"+str(len(cubicsfinal)))
        
    print('Finished.')
    fcubics.close()
    fplanes.close()

if __name__ == "__main__":
    main()