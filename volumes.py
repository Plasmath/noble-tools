import numpy as np
#Tools for working with the volumes of tetrahedra (and critical points/planes/curves)

#Find volume of tetrahedron with vertices a, b, c, and d (multiplied by 6 because that requires less calculation)
def volume(a,b,c,d):
    return abs(np.dot(a-d,np.cross(b-d,c-d)))

#Generates all possible subsets of 4 vertices containing a given point in a list of points
def maketets(l):
    z = l[0]
    return [[z,l[i+1],l[j+2],k] for i in range(len(l)-2) for j in range(i,len(l)-3) for k in l[j+3:]]

#Finds all tetrahedron volumes given a set of points
def findvols(points,cap):
    tets = maketets(points)
    return [min(round( volume(np.array(t[0]),
                              np.array(t[1]),
                              np.array(t[2]),
                              np.array(t[3])) ,12),cap) for t in tets]

#Finds minimum of tetrahedron volumes given a set of points
def minvol(points, cap):
    tets = maketets(points)
    m = cap #minimum value
    for t in tets:
        x = round( volume(np.array(t[0]),
                          np.array(t[1]),
                          np.array(t[2]),
                          np.array(t[3])) ,12)
        if x == 0:
            continue
        if x < 0.00000001: #abort when 'close enough' to 0, speeds up algorithm a lot
            return x
        if x < m:
            m = x
    return m

#version of volume function used for export programs
def symvol(p1,p2,p3,p4):
    x1, y1, z1 = p1
    x2, y2, z2 = p2
    x3, y3, z3 = p3
    x4, y4, z4 = p4
    return (x1*y2*z3 - x1*y2*z4 - x1*y3*z2 + x1*y3*z4 
          + x1*y4*z2 - x1*y4*z3 - x2*y1*z3 + x2*y1*z4 
          + x2*y3*z1 - x2*y3*z4 - x2*y4*z1 + x2*y4*z3 
          + x3*y1*z2 - x3*y1*z4 - x3*y2*z1 + x3*y2*z4 
          + x3*y4*z1 - x3*y4*z2 - x4*y1*z2 + x4*y1*z3 
          + x4*y2*z1 - x4*y2*z3 - x4*y3*z1 + x4*y3*z2)

#Add plane to critical plane
def addplane(l,p):
    sp = set(p)
    newl = [set(q) for q in l]
    for q in l:
        if len(q.intersection(set(sp))) > 2:
            sp = sp.union(q)
            newl.remove(q)
    newl.append(sp)
    
    return newl

#Combine critical planes together
def combineplanes(l1,l2):
    for p in l2:
        l1 = addplane(l1,p)
    return l1