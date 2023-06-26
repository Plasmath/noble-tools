import numpy as np
#Tools for working with the volumes of tetrahedra

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