import sympy as sp
from coordinates import tetrahedral, octahedral, icosahedral, doSymbolic
from volumes import symvol, maketets, combineplanes
from itertools import groupby

"""
Creates two files within the output file:
    - critical-planes.txt: faceting data containing critical planes
    - cubics.txt: the cubics in text form 
"""

"""Specifications for solving"""
army = icosahedral #Symmetry used
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
    for i in range(len(cubics)):
        if i % 1000 == 0:
            print('Finished matching',i,'tets out of',length)
        c = cubics[i]
        
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
    length = len(cubicsmatched)
    
    print("Factoring cubics...")
    cubicsfactored = [] #Separate cubics into their component factors
    for i in range(len(cubicsmatched)):
        if i % 1000 == 0:
            print('Finished factoring',i,'tets out of',length)
        c = cubicsmatched[i]
        
        fl = [ [factor,c[1]] for factor in factorize(c[0]) ]
        cubicsfactored += fl
    cubicsfactored = [k for k,v in groupby(sorted(cubicsfactored, key=repr))]
    length = len(cubicsfactored)
    
    print("Final round of matching...")
    cubicsfinal = [] #Factored cubics are matched together
    for i in range(len(cubicsfactored)):
        if i % 1000 == 0:
            print('Finished matching',i,'tets out of',length)
        c = cubicsfactored[i]
        
        newcubic = True
        for c1 in cubicsfinal:
            #Check if first and second cubic are the same cubic
            if c1[0] == c[0]:
                newcubic = False
                c1[1] = combineplanes(c1[1],c[1]) #Add second cubic's plane to this cubic
        if newcubic: #Adding new cubics to the list
            cubicsfinal.append(c)
    
    #Output to files
    fpairs = open("output/pairs.txt",'w') #Pairs of cubic plane curves to check for intersections of
    fcubics = open("output/cubics.txt",'w') #Cubics formatted for wolframscript
    fpyc = open("output/pycubics.txt","w") #Cubics formatted for python
    fplanes = open("output/critical-planes.txt",'w')
    for i in range(0,len(cubicsfinal)):
        fcubics.write(str(i) + ': ' + mps(cubicsfinal[i][0]) + "\n")
        fpyc.write(repr(cubicsfinal[i][0])+"\n")
        fplanes.write(str(i) + ': ' + str(cubicsfinal[i][1]).replace(' ','')+"\n")
        
        for j in range(i+1,len(cubicsfinal)):
            if hastripleintersection(cubicsfinal[i][1],cubicsfinal[j][1]):
                fpairs.write( str(i) + ' ' + str(j) + "\n" )
        
        if i%1000 == 0:
            print('Finished cubic type',str(i+1)+'/'+str(len(cubicsfinal)))
    
    print('Finished cubic type',str(len(cubicsfinal))+'/'+str(len(cubicsfinal)))
    
    print('Finished.')
    fpairs.close()
    fcubics.close()
    fplanes.close()

if __name__ == "__main__":
    main()