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
    coords = army(a,b)
    
    tets = maketets(range(len(coords))) #Tetrahedra as indices in coords, used for critical plane calculation
    
    cubics = []
    length = len(tets)
    for i in range(len(tets)):
        if i % 1000 == 0:
            print('Finished computing',i,'tets out of',length)
        tet = tets[i]
        cubics.append([vol(coords[tet[0]],coords[tet[1]],coords[tet[2]],coords[tet[3]]),[set(tet)]])
    
    print('Matching cubics...')
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
    
    #Now for the fun part: faceting.
    print("Faceting nobles...")
    nobles = [] #noblefaces with extra data
    for i in range(len(cubicsfinal)):
        noblefaces = [] #list of faces of nobles in this army
        
        cubic = cubicsfinal[i][0] #name of cubic        
        planes = cubicsfinal[i][1] #the critical planes of this intersection
        
        for pset in planes:
            cycles = noblecheck(pset, group) #faces of the nobles in this plane
            for c in cycles:
                if fullfilter(c, noblefaces, group): #filter out duplicates
                    noblefaces.append(c)
    
    #Export solutions, because these aren't offs this is pretty easily formatted
    fsols = open("noble-output/critical-curves.txt")
    fsols.write(nobles)
    print(nobles)

if __name__ == "__main__":
    main()