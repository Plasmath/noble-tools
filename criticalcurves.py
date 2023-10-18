import numpy as np
import sympy as sp
from coordinates import tetrahedral, octahedral, icosahedral, doSymbolic
from noblefaceting import tetgroup, octgroup, ikegroup
from volumes import symvol, maketets, combineplanes
from noblefaceting import noblecheck, fullfilter, generate
from itertools import groupby

"""Run export2d before running this program."""
"""Specifications for solving"""
army = icosahedral #Symmetry used
group = ikegroup #Group to use
extension = sp.sqrt(5) #Optional extension to factoring, use sp.sqrt(5) on icosahedral

#volume function
vol = lambda p1,p2,p3,p4 : sp.expand(symvol(p1,p2,p3,p4))

#Decomposes polynomial into polynomial factors
def factorize(poly):
    factored = [f for f in sp.factor(poly, extension = extension).args if not f.is_constant()] #remove constants because we don't care about them
    return [sp.factor_list(f)[1][0][0] for f in factored] #remove multiplicity too

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
    doSymbolic(True) #use symbolic coordinates
    
    a = sp.Symbol('a')
    b = sp.Symbol('b')
    sqrt = sp.sqrt
    coords = army(a,b)
    
    #Open list of cubics
    print("Importing file...")
    cubics = []
    for line in open("output/pycubics.txt").readlines():
        c = eval(line)
        cubics.append(c)
    print(len(cubics))
    
    #import critical planes
    print("Importing critical planes...")
    facetfile = open("output/critical-planes.txt").readlines()
    criticalplanes = []
    for planeline in facetfile:
        planes = eval(planeline.split(': ')[1]) #the leading index of the line is removed
        criticalplanes.append(planes)
    
    #Now for the fun part: faceting.
    print("Faceting nobles...")
    nobles = [] #noblefaces with extra data
    for i in range(len(cubics)):
        noblefaces = [] #list of faces of nobles in this army
        
        cubic = cubics[i] #name of cubic        
        planes = criticalplanes[i] #the critical planes of this intersection
        
        for pset in planes:
            cycles = noblecheck(pset, group) #faces of the nobles in this plane
            
            for c in cycles:
                if fullfilter(c, noblefaces, group): #filter out duplicates
                    noblefaces.append(c)
        
        if noblefaces != []:
            nobles.append([cubic,noblefaces])
    
    print(len(nobles),"nobles found.")
    print("Press enter to skip noble polyhedra without positive solutions.")
    
    doSymbolic(False) #disable for off export
    
    #Export solutions, ask for example solutions to cubic plane curves because it's easier
    for i in range(len(nobles)): #export nobles as OFF files   
        sol = input(str(i)+"/"+str(len(nobles))+"Solution for "+str(nobles[i][0]).replace("**","^").replace("sqrt(5)","\sqrt{5}")+" = 0 as ordered pair: ")
        if sol == "":
            continue
        sol = eval(sol)
        
        for n in nobles[i][1]:
            faces = generate(n, group)
            
            file = open("noble-output/noble-"+str(i)+".off", "w")
            print("noble-"+str(i), nobles[i][0], n)
            
            offcoords = army(sol[0],sol[1])
            
            #first two lines
            file.write("OFF\n")
            file.write(str(len(offcoords))+" "+str(len(faces))+" 0\n") #not bothering calculating edge count
            for c in offcoords:
                file.write(str(c[0])+" "+str(c[1])+" "+str(c[2])+"\n")
            
            for f in faces:
                s = "".join(str(k)+" " for k in f)
                s = str(len(f)) + " " + s + "\n"
                file.write(s)
            
            file.close()
    
    fsols = open("noble-output/critical-curves.txt","w")
    fsols.write(str(nobles))
    #print(nobles)
    print(len(nobles),"nobles found.")

if __name__ == "__main__":
    main()