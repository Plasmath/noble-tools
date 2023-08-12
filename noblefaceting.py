#Tetrahedral symmetry group
tetgroup = eval(open("groups/tetgroup.txt","r").read())

#Octahedral symmetry group
octgroup = eval(open("groups/octgroup.txt","r").read())

#Icosahedral symmetry group
ikegroup = eval(open("groups/ikegroup.txt","r").read())

#Various 1D symmetry groups
ratetgroup = eval(open("C:/Users/thepl/OneDrive/Documents/noble-tools/groups/1D/ratetgroup.txt","r").read())
tutgroup = eval(open("C:/Users/thepl/OneDrive/Documents/noble-tools/groups/1D/tutgroup.txt","r").read())
sircogroup = eval(open("C:/Users/thepl/OneDrive/Documents/noble-tools/groups/1D/sircogroup.txt","r").read())
ticgroup = eval(open("C:/Users/thepl/OneDrive/Documents/noble-tools/groups/1D/ticgroup.txt","r").read())
toegroup = eval(open("C:/Users/thepl/OneDrive/Documents/noble-tools/groups/1D/toegroup.txt","r").read())
sridgroup = eval(open("C:/Users/thepl/OneDrive/Documents/noble-tools/groups/1D/sridgroup.txt","r").read())
tidgroup = eval(open("C:/Users/thepl/OneDrive/Documents/noble-tools/groups/1D/tidgroup.txt","r").read())
tigroup = eval(open("C:/Users/thepl/OneDrive/Documents/noble-tools/groups/1D/tigroup.txt","r").read())

def permute(p,q): #permute p based on the elements of q
    size = len(p)
    
    r = []
    for i in range(size):
        r.append(q[p[i]])
    
    return tuple(r)

def generate(p,group): #copy plane vertices over symmetry group
    faces = []
    setfaces = []
    for i in group:
        perm = permute(p,i)
        if not set(perm) in setfaces:
            faces.append(perm)
            setfaces.append(set(perm))
    return faces

def isduplicate(f,faces): #determine if f is already within the list of faces (not including symmetry)
    i = f.index(0)
    g = list(f[i:]+f[:i])
    h = [0]+list(reversed(g[1:]))
    return (g in faces or h in faces)

def fullfilter(face,faces,group): #finds if face has a duplicate in faces
    for f in generate(face,group):
        if 0 in f:
            if isduplicate(f,faces):
                return False
    return True #return true if both tests are passed

def noblecheck(p, group): #checks for noble polyhedra within a plane
    #find edges in the original plane that intersect exactly 1 other plane in the symmetry group
    planes = generate(list(p), group)
    
    validedges = [] #edges that could be used to form nobles, forming a graph
    for plane in planes:
        e = sorted(tuple(p & set(plane))) #intersection of planes
        
        if len(e) == 2:
            validedges.append(tuple(e))
    
    #reformat validedges into a dictionary, for creating cycles
    edgedict = dict()
    edgedict[0] = []
    for edge in validedges:
        edgedict[edge[0]] = edgedict.setdefault(edge[0], []) + [edge[1]]
        edgedict[edge[1]] = edgedict.setdefault(edge[1], []) + [edge[0]]
    
    if len(edgedict[0]) < 2: #no cycles can be formed in this case, so we return no solution
        return []
    
    #find cycles of edges that will form the faces of nobles
    l = [[0]]
    cycles = []
    
    for i in range(len(edgedict)):
        lnew = []
        for poly in l:
            
            for point in edgedict[poly[-1]]:
                
                if point in poly:
                    if point == 0 and len(poly) > 3: #filter out tetrahedral compounds
                        cycles.append( poly )
                else:
                    lnew.append(poly + [point])
        l = lnew.copy()
    
    if cycles != []:
        print(p,validedges)
    
    #output results
    return cycles