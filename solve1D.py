from volumes import combineplanes
from noblefaceting import noblecheck, fullfilter, generate, tetgroup, octgroup, ikegroup
from coordinates import tetrahedral, octahedral, icosahedral
from sympy import Symbol

symmetry = octahedral #Army to use (should be equal to group)
group = octgroup #Group to use
minprecision = 8 #minimum digits of precision on solutions
minvalue = 1e-8 #minimum value of solutions, as some solutions at 0 are interpreted as small positive numbers

def evaluate(expr, aval, a):
    if type(expr) == int or type(expr) == float:
        return expr
    return expr.evalf(subs={a:aval})

def coordinates(aval, a, coords): #generate coordinates
    points = [ [evaluate(p[0], aval, a), evaluate(p[1], aval, a), evaluate(p[2], aval, a)] for p in coords ]
    return points

def collapsegroup(group, equals): #Merges equivalent points within group. May return error if done incorrectly.
    size = len(equals)
    
    #collapse the vertices of the group
    newgroup = []
    for i in range(size):
        exelement = list(equals[i])[0]        
        newgroup.append([None]*size)
        
        for j in range(size):
            equivclass = equals[j]
            mappedclass = { group[exelement][k] for k in equivclass }
            newgroup[i][j] = equals.index(mappedclass)
        
    return newgroup

def main():
    global group
    print("Creating group...")
    
    a = Symbol("a")
    
    coords, equals = eval(open("output/equivalent-points.txt").read())
    group = collapsegroup(group, equals)
    
    print("Importing intersection data...")
    
    inters = []
    for line in open("output/solutions.txt").readlines():
        
        if line[-1] == '\n': #remove newline if it exists
                line = line[:-1]
        
        if line == '{}': #case with no solutions
                inters.append([])
        else: #case with solutions
            values = []
            
            splitline = line[1:-1].split(',')
            
            for i in splitline:
                spliti = i.split('*^') #dealing with scientific notation
            
                #check for scientific notation
                if len(spliti) > 1:
                    exp = int(spliti[1])
                else:
                    exp = 0
                
                value, precision = spliti[0].split('`')
                
                if float(precision) < minprecision: #precision error
                    print('Not enough precision!',line)
                    continue
                
                solution = float(value) * 10**exp
                if solution > minvalue:
                    values.append(solution)
            
            inters.append(values)
    
    print("Importing critical planes...")
    
    #import critical planes
    facetfile = open("output/critical-planes.txt").readlines()
    
    criticalplanes = []
    
    for planeline in facetfile:
        planes = eval(planeline.split(': ')[1]) #the leading index of the line is removed
        
        criticalplanes.append(planes)
    
    #Separate shared critical planes from all the others
    shared = criticalplanes[0]
    cubicplanes = criticalplanes[1:]
    
    #Swap intersection points and their cubics in the data
    print("Reformatting stage 1...")
    intersdict = dict()
    for cubic in range(len(inters)):
        for coord in inters[cubic]:
            intersdict[coord] = intersdict.setdefault(coord,()) + (cubic,)
    
    #Turn lists of cubics into their critical planes, we now have all the data we need
    print("Reformatting stage 2...")
    intersdata = []
    for coord in intersdict:
        p1 = coord #intersection point
        p2 = intersdict[coord] #intersecting cubics
        p3 = shared.copy() #critical planes, includes shared planes
        for cubic in p2:
            p3 = combineplanes(p3, cubicplanes[cubic])
        intersdata.append([p1,p2,p3])
    
    #Now for the fun part: faceting.
    print("Faceting nobles...")
    nobles = [] #noblefaces with extra data
    for i in range(len(intersdata)):
        noblefaces = [] #list of faces of nobles in this army
        
        planes = intersdata[i][2] #the critical planes of this intersection
        extra = intersdata[i][:2] #other data
        
        for pset in planes:
            cycles = noblecheck(pset, group) #faces of the nobles in this plane
            
            for c in cycles:
                if fullfilter(c, noblefaces, group): #filter out duplicates
                    noblefaces.append(c)
                    nobles.append(extra+[c])
    
    print("Found",len(nobles),"nobles.")
    
    for i in range(len(nobles)):
        n = nobles[i][2]
        faces = generate(n, group)
        
        file = open("noble-output/noble-"+str(i)+".off", "w")
        file.write("OFF\n")
        file.write(str(len(coords))+" "+str(len(faces))+" 0\n") #not bothering calculating edge count
        
        offcoords = coordinates(nobles[i][0], a, coords)
        for c in offcoords:
            file.write(str(c[0])+" "+str(c[1])+" "+str(c[2])+"\n")
        
        for f in faces:
            s = "".join(str(k)+" " for k in f)
            s = str(len(f)) + " " + s + "\n"
            file.write(s)
        
        file.close()

if __name__ == "__main__":
    main()