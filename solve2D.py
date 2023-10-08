from volumes import combineplanes
from coordinates import tetrahedral, octahedral, icosahedral, doSymbolic
from noblefaceting import noblecheck, fullfilter, generate, tetgroup, octgroup, ikegroup
import os

"""Run export2d and intersect2D before running this program."""
"""Specifications for solving"""
army = octahedral
group = octgroup
minprecision = 8 #minimum digits of precision on solutions
minvalue = 1e-8 #minimum value of solutions, as some solutions at 0 are interpreted as small positive numbers

def main():
    global group
    doSymbolic(False) #Use decimal coordinates
    
    print("Importing intersection data...")
    
    directory = os.fsencode("output/solutions")
    
    inters = []
    for file in os.listdir(directory):
        for line in open("output/solutions/"+file.decode("utf-8")).readlines():
            
            if line[-1] == '\n': #remove newline if it exists
                line = line[:-1]
            
            if line == '{}': #case with no solutions
                inters.append([])
            
            else: #case with solutions
                splitline = line[2:-2].split('}, {')
                
                pairs = []
                for i in splitline:
                    
                    stringpair = i.split(',')
                    pair = [stringpair[0].split('*^'),
                            stringpair[1].split('*^')]
                    
                    #check for floating point
                    if len(pair[0]) > 1:
                        exp0 = int(pair[0][1])
                    else:
                        exp0 = 0
                    if len(pair[1]) > 1:
                        exp1 = int(pair[1][1])
                    else:
                        exp1 = 0
                    pair[0] = float( pair[0][0].split('`')[0] ) * 10**exp0
                    pair[1] = float( pair[1][0].split('`')[0] ) * 10**exp1
                    
                    if pair[0] > 1e-8 and pair[1] > 1e-8:
                        pairs.append(tuple(pair))
                
                inters.append(pairs)
    
    print("Importing critical pairs...")
    pairs = [tuple(int(i) for i in p.split(" ")) for p in open("output/pairs.txt").read().split("\n")[:-1]]
    
    print("Importing critical planes...")
    facetfile = open("output/critical-planes.txt").readlines()
    
    cubicplanes = []
    
    for planeline in facetfile:
        planes = eval(planeline.split(': ')[1]) #the leading index of the line is removed
        
        cubicplanes.append(planes) 
    
    #Swap intersection points and pairs in the data
    print("Reformatting stage 1...")
    intersdict = dict()
    for cubic in range(len(inters)):
        for coord in inters[cubic]:
            intersdict[coord] = intersdict.setdefault(coord,()) + (pairs[cubic],)
    
    #Turn lists of pairs into their critical planes, we now have all the data we need
    print("Reformatting stage 2...")
    intersdata = []
    for coord in intersdict:
        p1 = coord #intersection point
        p2 = intersdict[coord] #intersecting cubics
        p3 = [] #critical planes
        for pair in p2:
            p3 = combineplanes(p3, cubicplanes[pair[0]]+cubicplanes[pair[1]])
        intersdata.append([p1,p2,p3])
    
    #Now for the fun part: faceting.
    print("Faceting nobles...")
    nobles = [] #noblefaces with extra data
    for i in range(len(intersdata)):
        noblefaces = [] #list of faces of nobles in this army
        
        planes = intersdata[i][2] #the critical planes of this intersection
        extra = intersdata[i][:2] #other data
        
        for pset in planes:
            cycles = noblecheck(pset, group, minsize=5) #faces of the nobles in this plane
            for c in cycles:
                if fullfilter(c, noblefaces, group): #filter out duplicates
                    noblefaces.append(c)
                    nobles.append(extra+[c])
    
    print("Found",len(nobles),"nobles.")
    summary = open("noble-output/summary.txt", "w")
    for i in range(len(nobles)):
        n = nobles[i][2]
        faces = generate(n, group)
        
        print("noble-"+str(i), n, nobles[i][0])
        
        file = open("noble-output/noble-"+str(i)+".off", "w")
        
        offcoords = army(nobles[i][0][0], nobles[i][0][1])
        
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
        
        summary.write("noble-"+str(i)+" "+str(nobles[i])+"\n")
    
if __name__ == "__main__":
    main()