import copy #used in faceting

#Tetrahedral symmetry group
tetgroup = eval(open("groups/tetgroup.txt","r").read())

#Octahedral symmetry group
octgroup = eval(open("groups/octgroup.txt","r").read())

#Icosahedral symmetry group
ikegroup = eval(open("groups/ikegroup.txt","r").read())

#Various 1D symmetry groups
ratetgroup = eval(open("groups/1D/ratetgroup.txt","r").read())
tutgroup = eval(open("groups/1D/tutgroup.txt","r").read())
sircogroup = eval(open("groups/1D/sircogroup.txt","r").read())
ticgroup = eval(open("groups/1D/ticgroup.txt","r").read())
toegroup = eval(open("groups/1D/toegroup.txt","r").read())
sridgroup = eval(open("groups/1D/sridgroup.txt","r").read())
tidgroup = eval(open("groups/1D/tidgroup.txt","r").read())
tigroup = eval(open("groups/1D/tigroup.txt","r").read())

#Chiral 1D symmetry groups
kiratetgroup = eval(open("groups/1D/kiratetgroup.txt","r").read())
kitutgroup = eval(open("groups/1D/kitutgroup.txt","r").read())
kisircogroup = eval(open("groups/1D/kisircogroup.txt","r").read())
kiticgroup = eval(open("groups/1D/kiticgroup.txt","r").read())
kitoegroup = eval(open("groups/1D/kitoegroup.txt","r").read())
kisridgroup = eval(open("groups/1D/kisridgroup.txt","r").read())
kitidgroup = eval(open("groups/1D/kitidgroup.txt","r").read())
kitigroup = eval(open("groups/1D/kitigroup.txt","r").read())

#Pyritohedral 1D symmetry groups
pysircogroup = eval(open("groups/1D/pysircogroup.txt","r").read())
pyticgroup = eval(open("groups/1D/pyticgroup.txt","r").read())

def permute(p,q): #permute p based on the elements of q
    size = len(p)
    
    r = []
    for i in range(size):
        r.append(q[p[i]])
    
    return tuple(r)

def syms(p,group): #(non-identity) symmetries of group that fix a plane p
    planesyms = []
    for i in group:
        perm = permute(p,i)
        if set(perm) == set(p) and list(range(len(group))) != i:
            planesyms.append(i)
    return planesyms

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

def noblecheck(P, group, minsize=4): #checks for noble polyhedra within a plane whose polygons have at least minsize sides
    p = list(P)
    #find edges in the original plane that intersect exactly 1 other plane in the symmetry group
    planes = generate(p, group)
    planesyms = syms(p, group)
    
    validedges = [] #sets of edges that could be used to form nobles, forming a graph
    for plane in planes:
        e = tuple(sorted(tuple(P & set(plane)))) #intersection of planes
        if len(e) == 2:
            pair = [ e, tuple(sorted((p[plane.index(e[0])], p[plane.index(e[1])]))) ]
            validedges.append(pair)
    
    #reformat validedges into a dictionary, for creating cycles
    edgedict = dict()
    identdict = dict() #edges equivalent under symmetry
    edgedict[0] = []
    for edge in validedges:
        if edge[0] != edge[1]:
            identdict[edge[0]] = edge[1]
        else:
            identdict[edge[0]] = identdict.setdefault(edge[0],[])
        
        edgedict[edge[0][0]] = set(list(edgedict.setdefault(edge[0][0], set())) + [edge[0][1]])
        edgedict[edge[0][1]] = set(list(edgedict.setdefault(edge[0][1], set())) + [edge[0][0]])
    
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
                    if point == 0 and len(poly) >= minsize and [0]+list(reversed(poly[1:])) not in cycles: #minsize filter
                        cycles.append( poly )
                else:
                    lnew.append(poly + [point])
        l = lnew.copy()
    
    #filter out fake cycles that have equivalent edges not in the cycle
    finalcycles = []
    for c in cycles:
        edges = [tuple(sorted([c[i],c[(i+1)%len(c)]])) for i in range(len(c))] #edges of cycle
        
        idents = [identdict[e] for e in edges if identdict[e] not in edges and identdict[e] != []] #identical edges with no corresponding pair
        
        for sym in planesyms:
            #filter out irremovable exotic faces
            permuted = permute(c, sym)
            permedges = [tuple(sorted([permuted[i],permuted[(i+1)%len(c)]])) for i in range(len(c))]
            
            if len(set(edges) & set(permedges)) > 0 and set(edges) != set(permedges):
                idents = ["exotic"]
                break
            
            idents = [e for e in idents if e not in permedges] #filter out edges in equivalent faces (found in fissary duals)
        
        if idents == []:
            finalcycles.append(c)
    
    #output results
    return finalcycles