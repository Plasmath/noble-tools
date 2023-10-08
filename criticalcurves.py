import numpy as np
import sympy as sp
from coordinates import tetrahedral, octahedral, icosahedral, doSymbolic
from noblefaceting import tetgroup, octgroup, ikegroup
from volumes import symvol, maketets, combineplanes
from noblefaceting import noblecheck, fullfilter, generate
from itertools import groupby

"""Run export2d before running this program."""
"""Specifications for solving"""
army = octahedral #Symmetry used
group = octgroup #Group to use
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
    
    #Export solutions, because these aren't offs this is pretty easily formatted
    fsols = open("noble-output/critical-curves.txt","w")
    fsols.write(str(nobles))
    print(nobles)
    print(len(nobles),"nobles found.")

if __name__ == "__main__":
    main()