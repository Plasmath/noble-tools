from math import sqrt
#Program for obtaining coordinates of noble polyhedra hulls

def tetrahedral(a,b): #Requires a > 0, b > 0 to obtain unique coordinates
    return [(1,(1+a),(1+a+b)), ((1+a),1,(1+a+b)), ((1+a),(1+a+b),1), (1,(1+a+b),(1+a)), ((1+a+b),1,(1+a)), ((1+a+b),(1+a),1),
            (-1,-(1+a),(1+a+b)), (-(1+a),-1,(1+a+b)), (-(1+a),-(1+a+b),1), (-1,-(1+a+b),(1+a)), (-(1+a+b),-1,(1+a)), (-(1+a+b),-(1+a),1),
            (-1,(1+a),-(1+a+b)), (-(1+a),1,-(1+a+b)), (-(1+a),(1+a+b),-1), (-1,(1+a+b),-(1+a)), (-(1+a+b),1,-(1+a)), (-(1+a+b),(1+a),-1),
            (1,-(1+a),-(1+a+b)), ((1+a),-1,-(1+a+b)), ((1+a),-(1+a+b),-1), (1,-(1+a+b),-(1+a)), ((1+a+b),-1,-(1+a)), ((1+a+b),-(1+a),-1)]

def octahedral(a,b): #Requires a > 1, 1 < b < a
    return [(a,b,1), (b,a,1), (b,1,a), (a,1,b), (1,a,b), (1,b,a),
            (-a,b,1), (-b,a,1), (-b,1,a), (-a,1,b), (-1,a,b), (-1,b,a),
            (a,-b,1), (b,-a,1), (b,-1,a), (a,-1,b), (1,-a,b), (1,-b,a),
            (a,b,-1), (b,a,-1), (b,1,-a), (a,1,-b), (1,a,-b), (1,b,-a),
            (-a,-b,1), (-b,-a,1), (-b,-1,a), (-a,-1,b), (-1,-a,b), (-1,-b,a),
            (-a,b,-1), (-b,a,-1), (-b,1,-a), (-a,1,-b), (-1,a,-b), (-1,b,-a),
            (a,-b,-1), (b,-a,-1), (b,-1,-a), (a,-1,-b), (1,-a,-b), (1,-b,-a),
            (-a,-b,-1), (-b,-a,-1), (-b,-1,-a), (-a,-1,-b), (-1,-a,-b), (-1,-b,-a)]

g = (sqrt(5)+1)/2 #golden ratio
G = (sqrt(5)+3)/2 #golden ratio plus 1

def icosahedral(a,b):
    return [(1, a, a*g+2*b*g+G),(a, a*g+2*b*g+G, 1),(a*g+2*b*g+G, 1, a),
            (b*g+1, a+b, a*g+b*G+G),(a*g+b*G+G, b*g+1, a+b),(a+b, a*g+b*G+G, b*g+1),
            (a*g+b*g+1, b, a+b*G+G),(b, a+b*G+G, a*g+b*g+1),(a+b*G+G, a*g+b*g+1, b),
            (b*g+g, a+b+g, a*g+b*G+g),(a+b+g, a*g+b*G+g, b*g+g),(a*g+b*G+g, b*g+g, a+b+g),
            (b+g, a+b*G+g, a*g+b*g+g),(a+b*G+g, a*g+b*g+g, b+g),(a*g+b*g+g, b+g, a+b*G+g),
            (-1, a, a*g+2*b*g+G),(-a, a*g+2*b*g+G, 1),(-a*g-2*b*g-G, 1, a),
            (-b*g-1, a+b, a*g+b*G+G),(-a*g-b*G-G, b*g+1, a+b),(-a-b, a*g+b*G+G, b*g+1),
            (-a*g-b*g-1, b, a+b*G+G),(-b, a+b*G+G, a*g+b*g+1),(-a-b*G-G, a*g+b*g+1, b),
            (-b*g-g, a+b+g, a*g+b*G+g),(-a-b-g, a*g+b*G+g, b*g+g),(-a*g-b*G-g, b*g+g, a+b+g),
            (-b-g, a+b*G+g, a*g+b*g+g),(-a-b*G-g, a*g+b*g+g, b+g),(-a*g-b*g-g, b+g, a+b*G+g),
            (1, -a, a*g+2*b*g+G),(a, -a*g-2*b*g-G, 1),(a*g+2*b*g+G, -1, a),
            (b*g+1, -a-b, a*g+b*G+G),(a*g+b*G+G, -b*g-1, a+b),(a+b, -a*g-b*G-G, b*g+1),
            (a*g+b*g+1, -b, a+b*G+G),(b, -a-b*G-G, a*g+b*g+1),(a+b*G+G, -a*g-b*g-1, b),
            (b*g+g, -a-b-g, a*g+b*G+g),(a+b+g, -a*g-b*G-g, b*g+g),(a*g+b*G+g, -b*g-g, a+b+g),
            (b+g, -a-b*G-g, a*g+b*g+g),(a+b*G+g, -a*g-b*g-g, b+g),(a*g+b*g+g, -b-g, a+b*G+g),
            (-1, -a, a*g+2*b*g+G),(-a, -a*g-2*b*g-G, 1),(-a*g-2*b*g-G, -1, a),
            (-b*g-1, -a-b, a*g+b*G+G),(-a*g-b*G-G, -b*g-1, a+b),(-a-b, -a*g-b*G-G, b*g+1),
            (-a*g-b*g-1, -b, a+b*G+G),(-b, -a-b*G-G, a*g+b*g+1),(-a-b*G-G, -a*g-b*g-1, b),
            (-b*g-g, -a-b-g, a*g+b*G+g),(-a-b-g, -a*g-b*G-g, b*g+g),(-a*g-b*G-g, -b*g-g, a+b+g),
            (-b-g, -a-b*G-g, a*g+b*g+g),(-a-b*G-g, -a*g-b*g-g, b+g),(-a*g-b*g-g, -b-g, a+b*G+g),
            (1, a, -a*g-2*b*g-G),(a, a*g+2*b*g+G, -1),(a*g+2*b*g+G, 1, -a),
            (b*g+1, a+b, -a*g-b*G-G),(a*g+b*G+G, b*g+1, -a-b),(a+b, a*g+b*G+G, -b*g-1),
            (a*g+b*g+1, b, -a-b*G-G),(b, a+b*G+G, -a*g-b*g-1),(a+b*G+G, a*g+b*g+1, -b),
            (b*g+g, a+b+g, -a*g-b*G-g),(a+b+g, a*g+b*G+g, -b*g-g),(a*g+b*G+g, b*g+g, -a-b-g),
            (b+g, a+b*G+g, -a*g-b*g-g),(a+b*G+g, a*g+b*g+g, -b-g),(a*g+b*g+g, b+g, -a-b*G-g),
            (-1, a, -a*g-2*b*g-G),(-a, a*g+2*b*g+G, -1),(-a*g-2*b*g-G, 1, -a),
            (-b*g-1, a+b, -a*g-b*G-G),(-a*g-b*G-G, b*g+1, -a-b),(-a-b, a*g+b*G+G, -b*g-1),
            (-a*g-b*g-1, b, -a-b*G-G),(-b, a+b*G+G, -a*g-b*g-1),(-a-b*G-G, a*g+b*g+1, -b),
            (-b*g-g, a+b+g, -a*g-b*G-g),(-a-b-g, a*g+b*G+g, -b*g-g),(-a*g-b*G-g, b*g+g, -a-b-g),
            (-b-g, a+b*G+g, -a*g-b*g-g),(-a-b*G-g, a*g+b*g+g, -b-g),(-a*g-b*g-g, b+g, -a-b*G-g),
            (1, -a, -a*g-2*b*g-G),(a, -a*g-2*b*g-G, -1),(a*g+2*b*g+G, -1, -a),
            (b*g+1, -a-b, -a*g-b*G-G),(a*g+b*G+G, -b*g-1, -a-b),(a+b, -a*g-b*G-G, -b*g-1),
            (a*g+b*g+1, -b, -a-b*G-G),(b, -a-b*G-G, -a*g-b*g-1),(a+b*G+G, -a*g-b*g-1, -b),
            (b*g+g, -a-b-g, -a*g-b*G-g),(a+b+g, -a*g-b*G-g, -b*g-g),(a*g+b*G+g, -b*g-g, -a-b-g),
            (b+g, -a-b*G-g, -a*g-b*g-g),(a+b*G+g, -a*g-b*g-g, -b-g),(a*g+b*g+g, -b-g, -a-b*G-g),
            (-1, -a, -a*g-2*b*g-G),(-a, -a*g-2*b*g-G, -1),(-a*g-2*b*g-G, -1, -a),
            (-b*g-1, -a-b, -a*g-b*G-G),(-a*g-b*G-G, -b*g-1, -a-b),(-a-b, -a*g-b*G-G, -b*g-1),
            (-a*g-b*g-1, -b, -a-b*G-G),(-b, -a-b*G-G, -a*g-b*g-1),(-a-b*G-G, -a*g-b*g-1, -b),
            (-b*g-g, -a-b-g, -a*g-b*G-g),(-a-b-g, -a*g-b*G-g, -b*g-g),(-a*g-b*G-g, -b*g-g, -a-b-g),
            (-b-g, -a-b*G-g, -a*g-b*g-g),(-a-b*G-g, -a*g-b*g-g, -b-g),(-a*g-b*g-g, -b-g, -a-b*G-g)]

#merge identical points together
def mergepoints(points):
    threshold = 1e-5 #maximum distance to merge
    
    newpoints = []
    for p in points:
        if all(abs(p[0]-q[0])+abs(p[1]-q[1])+abs(p[2]-q[2]) > threshold for q in newpoints):
            newpoints.append(p)
    return newpoints