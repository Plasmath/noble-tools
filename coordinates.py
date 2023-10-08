from math import sqrt
from sympy import sqrt as sp_sqrt
#Program for obtaining coordinates of noble polyhedra hulls

doSymbolicBool = False #Whether or not to use Sympy notation or floats
def doSymbolic(t): 
    global doSymbolicBool
    doSymbolicBool = t

def tetrahedral(a,b): #Requires a > 0, b > 0 to obtain unique coordinates
    return [(1,(1+a),(1+a+b)), ((1+a),1,(1+a+b)), ((1+a),(1+a+b),1), (1,(1+a+b),(1+a)), ((1+a+b),1,(1+a)), ((1+a+b),(1+a),1),
            (-1,-(1+a),(1+a+b)), (-(1+a),-1,(1+a+b)), (-(1+a),-(1+a+b),1), (-1,-(1+a+b),(1+a)), (-(1+a+b),-1,(1+a)), (-(1+a+b),-(1+a),1),
            (-1,(1+a),-(1+a+b)), (-(1+a),1,-(1+a+b)), (-(1+a),(1+a+b),-1), (-1,(1+a+b),-(1+a)), (-(1+a+b),1,-(1+a)), (-(1+a+b),(1+a),-1),
            (1,-(1+a),-(1+a+b)), ((1+a),-1,-(1+a+b)), ((1+a),-(1+a+b),-1), (1,-(1+a+b),-(1+a)), ((1+a+b),-1,-(1+a)), ((1+a+b),-(1+a),-1)]

def snit(a,b):
    return [((a-1),(a+1),(a+b+1)), ((a+1),(a+b+1),(a-1)), ((a+b+1),(a-1),(a+1)),
            ((a-1),-(a+1),-(a+b+1)), ((a+1),-(a+b+1),-(a-1)), ((a+b+1),-(a-1),-(a+1)),
            (-(a-1),(a+1),-(a+b+1)), (-(a+1),(a+b+1),-(a-1)), (-(a+b+1),(a-1),-(a+1)),
            (-(a-1),-(a+1),(a+b+1)), (-(a+1),-(a+b+1),(a-1)), (-(a+b+1),-(a-1),(a+1))]

def ratet(a):
    return [((a-1),(a+1),(a+1)), ((a+1),(a+1),(a-1)), ((a+1),(a-1),(a+1)),
            ((a-1),-(a+1),-(a+1)), ((a+1),-(a+1),-(a-1)), ((a+1),-(a-1),-(a+1)),
            (-(a-1),(a+1),-(a+1)), (-(a+1),(a+1),-(a-1)), (-(a+1),(a-1),-(a+1)),
            (-(a-1),-(a+1),(a+1)), (-(a+1),-(a+1),(a-1)), (-(a+1),-(a-1),(a+1))]

def tut(b):
    return [(-1,1,(+b+1)), (1,(+b+1),-1), ((+b+1),-1,1),
            (-1,-1,-(+b+1)), (1,-(+b+1),1), ((+b+1),1,-1),
            (1,1,-(+b+1)), (-1,(+b+1),1), (-(+b+1),-1,-1),
            (1,-1,(+b+1)), (-1,-(+b+1),-1), (-(+b+1),1,1)]

def octahedral(a,b): #Requires a > 0, b > 0
    return [( a+b+1, a+1, 1),( a+1, a+b+1, 1),( a+1, 1, a+b+1),( a+b+1, 1, a+1),( 1, a+b+1, a+1),( 1, a+1, a+b+1),
            (-a-b-1, a+1, 1),(-a-1, a+b+1, 1),(-a-1, 1, a+b+1),(-a-b-1, 1, a+1),(-1, a+b+1, a+1),(-1, a+1, a+b+1),
            ( a+b+1,-a-1, 1),( a+1,-a-b-1, 1),( a+1,-1, a+b+1),( a+b+1,-1, a+1),( 1,-a-b-1, a+1),( 1,-a-1, a+b+1),
            (-a-b-1,-a-1, 1),(-a-1,-a-b-1, 1),(-a-1,-1, a+b+1),(-a-b-1,-1, a+1),(-1,-a-b-1, a+1),(-1,-a-1, a+b+1),
            ( a+b+1, a+1,-1),( a+1, a+b+1,-1),( a+1, 1,-a-b-1),( a+b+1, 1,-a-1),( 1, a+b+1,-a-1),( 1, a+1,-a-b-1),
            (-a-b-1, a+1,-1),(-a-1, a+b+1,-1),(-a-1, 1,-a-b-1),(-a-b-1, 1,-a-1),(-1, a+b+1,-a-1),(-1, a+1,-a-b-1),
            ( a+b+1,-a-1,-1),( a+1,-a-b-1,-1),( a+1,-1,-a-b-1),( a+b+1,-1,-a-1),( 1,-a-b-1,-a-1),( 1,-a-1,-a-b-1),
            (-a-b-1,-a-1,-1),(-a-1,-a-b-1,-1),(-a-1,-1,-a-b-1),(-a-b-1,-1,-a-1),(-1,-a-b-1,-a-1),(-1,-a-1,-a-b-1)]

def sirco(b):
    return [( b+1, 1, 1),( 1, b+1, 1),( 1, 1, b+1),
            (-b-1, 1, 1),(-1, b+1, 1),(-1, 1, b+1),
            ( b+1,-1, 1),( 1,-b-1, 1),( 1,-1, b+1),
            (-b-1,-1, 1),(-1,-b-1, 1),(-1,-1, b+1),
            ( b+1, 1,-1),( 1, b+1,-1),( 1, 1,-b-1),
            (-b-1, 1,-1),(-1, b+1,-1),(-1, 1,-b-1),
            ( b+1,-1,-1),( 1,-b-1,-1),( 1,-1,-b-1),
            (-b-1,-1,-1),(-1,-b-1,-1),(-1,-1,-b-1)]

def tic(a):
    return [( a+1, a+1, 1),( a+1, 1, a+1),( 1, a+1, a+1),
            (-a-1, a+1, 1),(-a-1, 1, a+1),(-1, a+1, a+1),
            ( a+1,-a-1, 1),( a+1,-1, a+1),( 1,-a-1, a+1),
            (-a-1,-a-1, 1),(-a-1,-1, a+1),(-1,-a-1, a+1),
            ( a+1, a+1,-1),( a+1, 1,-a-1),( 1, a+1,-a-1),
            (-a-1, a+1,-1),(-a-1, 1,-a-1),(-1, a+1,-a-1),
            ( a+1,-a-1,-1),( a+1,-1,-a-1),( 1,-a-1,-a-1),
            (-a-1,-a-1,-1),(-a-1,-1,-a-1),(-1,-a-1,-a-1)]

def toe(a):
    return [( a+1, a, 0),( a+1,-a, 0),( a+1, 0, a),( a+1, 0,-a),
            (-a-1, a, 0),(-a-1,-a, 0),(-a-1, 0, a),(-a-1, 0,-a),
            ( a, a+1, 0),( a,-a-1, 0),( a, 0, a+1),( a, 0,-a-1),
            (-a, a+1, 0),(-a,-a-1, 0),(-a, 0, a+1),(-a, 0,-a-1),
            ( 0, a+1, a),( 0,-a-1, a),( 0, a+1,-a),( 0,-a-1,-a),
            ( 0, a, a+1),( 0,-a, a+1),( 0, a,-a-1),( 0,-a,-a-1)]

print(ratet(2))

def snic(a,b): #Chiral octahedral. Requires a > 1, 1 < b < a
    return [(a,b,1),(-a,-b,1),(-a,b,-1),(a,-b,-1),
            (b,1,a),(-b,-1,a),(-b,1,-a),(b,-1,-a),
            (1,a,b),(-1,-a,b),(-1,a,-b),(1,-a,-b),
            (-b,a,1),(b,-a,1),(b,a,-1),(-b,-a,-1),
            (-a,1,b),(a,-1,b),(a,1,-b),(-a,-1,-b),
            (-1,b,a),(1,-b,a),(1,b,-a),(-1,-b,-a)]

def pyritohedral(a,b): #Requires a > 1, 1 < b < a
    return [(a,b,1),(1,a,b),(b,1,a),(-a,b,1),(-1,a,b),(-b,1,a),
            (a,-b,1),(1,-a,b),(b,-1,a),(-a,-b,1),(-1,-a,b),(-b,-1,a),
            (a,b,-1),(1,a,-b),(b,1,-a),(-a,b,-1),(-1,a,-b),(-b,1,-a),
            (a,-b,-1),(1,-a,-b),(b,-1,-a),(-a,-b,-1),(-1,-a,-b),(-b,-1,-a)]

g = (sqrt(5)+1)/2 #golden ratio
G = (sqrt(5)+3)/2 #golden ratio plus 1
def makesymb(): #b is true/false
    global g
    global G
    if doSymbolicBool:
        g = (sp_sqrt(5)+1)/2
        G = (sp_sqrt(5)+3)/2
    else:
        g = (sqrt(5)+1)/2
        G = (sqrt(5)+3)/2

def icosahedral(a,b):
    makesymb()
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

def srid(a):
    makesymb()
    return [(1, a, a*g+G),(a, a*g+G, 1),(a*g+G, 1, a),
            (g, a+g, a*g+g),(a+g, a*g+g, g),(a*g+g, g, a+g),
            (-1, a, a*g+G),(-a, a*g+G, 1),(-a*g-G, 1, a),
            (-g, a+g, a*g+g),(-a-g, a*g+g, g),(-a*g-g, g, a+g),
            (1, -a, a*g+G),(a, -a*g-G, 1),(a*g+G, -1, a),
            (g, -a-g, a*g+g),(a+g, -a*g-g, g),(a*g+g, -g, a+g),
            (-1, -a, a*g+G),(-a, -a*g-G, 1),(-a*g-G, -1, a),
            (-g, -a-g, a*g+g),(-a-g, -a*g-g, g),(-a*g-g, -g, a+g),
            (1, a, -a*g-G),(a, a*g+G, -1),(a*g+G, 1, -a),
            (g, a+g, -a*g-g),(a+g, a*g+g, -g),(a*g+g, g, -a-g),
            (-1, a, -a*g-G),(-a, a*g+G, -1),(-a*g-G, 1, -a),
            (-g, a+g, -a*g-g),(-a-g, a*g+g, -g),(-a*g-g, g, -a-g),
            (1, -a, -a*g-G),(a, -a*g-G, -1),(a*g+G, -1, -a),
            (g, -a-g, -a*g-g),(a+g, -a*g-g, -g),(a*g+g, -g, -a-g),
            (-1, -a, -a*g-G),(-a, -a*g-G, -1),(-a*g-G, -1, -a),
            (-g, -a-g, -a*g-g),(-a-g, -a*g-g, -g),(-a*g-g, -g, -a-g),
            (0, a+G, a*g+1), (0, -a-G, a*g+1), (0, a+G, -a*g-1), (0, -a-G, -a*g-1),
            (a*g+1, 0, a+G), (a*g+1, 0, -a-G), (-a*g-1, 0, a+G), (-a*g-1, 0, -a-G),
            (a+G, a*g+1, 0), (a+G, -a*g-1, 0), (-a-G, a*g+1, 0), (-a-G, -a*g-1, 0)]

def tid(b):
    makesymb()
    return [(0, 2*b*g+G, 1),(0, -2*b*g-G, 1),(0, 2*b*g+G, -1),(0, -2*b*g-G, -1),
            (1, 0, 2*b*g+G),(1, 0, -2*b*g-G),(-1, 0, 2*b*g+G),(-1, 0, -2*b*g-G),
            (2*b*g+G, 1, 0),(2*b*g+G, -1, 0),(-2*b*g-G, 1, 0),(-2*b*g-G, -1, 0),
            (b*g+1, b, b*G+G),(b*g+1, -b, b*G+G),(b*g+1, b, -b*G-G),(b*g+1, -b, -b*G-G),
            (-b*g-1, b, b*G+G),(-b*g-1, -b, b*G+G),(-b*g-1, b, -b*G-G),(-b*g-1, -b, -b*G-G),
            (b*G+G, b*g+1, b),(b*G+G, -b*g-1, b),(b*G+G, b*g+1, -b), (b*G+G, -b*g-1, -b),
            (-b*G-G, b*g+1, b),(-b*G-G, -b*g-1, b),(-b*G-G, b*g+1, -b),(-b*G-G, -b*g-1, -b),
            (b, b*G+G, b*g+1),(b, -b*G-G, b*g+1),(b, b*G+G, -b*g-1),(b, -b*G-G, -b*g-1),
            (-b, b*G+G, b*g+1),(-b, -b*G-G, b*g+1),(-b, b*G+G, -b*g-1),(-b, -b*G-G, -b*g-1),
            (b*g+g, b+g, b*G+g),(b*g+g, -b-g, b*G+g),(b*g+g, b+g, -b*G-g),(b*g+g, -b-g, -b*G-g),
            (-b*g-g, b+g, b*G+g),(-b*g-g, -b-g, b*G+g),(-b*g-g, b+g, -b*G-g),(-b*g-g, -b-g, -b*G-g),
            (b+g, b*G+g, b*g+g),(b+g, -b*G-g, b*g+g),(b+g, b*G+g, -b*g-g),(b+g, -b*G-g, -b*g-g),
            (-b-g, b*G+g, b*g+g),(-b-g, -b*G-g, b*g+g),(-b-g, b*G+g, -b*g-g),(-b-g, -b*G-g, -b*g-g),
            (b*G+g, b*g+g, b+g),(b*G+g, -b*g-g, b+g),(b*G+g, b*g+g, -b-g),(b*G+g, -b*g-g, -b-g),
            (-b*G-g, b*g+g, b+g),(-b*G-g, -b*g-g, b+g),(-b*G-g, b*g+g, -b-g),(-b*G-g, -b*g-g, -b-g)]

def ti(a):
    makesymb()
    return [(0, a, a*g+2*g),(0, -a, a*g+2*g),(0, a, -a*g-2*g),(0, -a, -a*g-2*g),
            (a*g+2*g, 0, a),(-a*g-2*g, 0, a),(a*g+2*g, 0, -a),(-a*g-2*g, 0, -a),
            (a, a*g+2*g, 0),(-a, a*g+2*g, 0),(a, -a*g-2*g, 0),(-a, -a*g-2*g, 0),
            (g, a+1, a*g+G),(g, -a-1, a*g+G),(g, a+1, -a*g-G),(g, -a-1, -a*g-G),
            (-g, a+1, a*g+G),(-g, -a-1, a*g+G),(-g, a+1, -a*g-G),(-g, -a-1, -a*g-G),
            (a+1, a*g+G, g),(a+1, -a*g-G, g),(a+1, a*g+G, -g),(a+1, -a*g-G, -g),
            (-a-1, a*g+G, g),(-a-1, -a*g-G, g),(-a-1, a*g+G, -g),(-a-1, -a*g-G, -g),
            (1, a+G, a*g+g),(1, -a-G, a*g+g),(1, a+G, -a*g-g),(1, -a-G, -a*g-g),
            (-1, a+G, a*g+g),(-1, -a-G, a*g+g),(-1, a+G, -a*g-g),(-1, -a-G, -a*g-g),
            (a*g+G, g, a+1),(a*g+G, -g, a+1),(a*g+G, g, -a-1),(a*g+G, -g, -a-1),
            (-a*g-G, g, a+1),(-a*g-G, -g, a+1),(-a*g-G, g, -a-1),(-a*g-G, -g, -a-1),
            (a*g+g, 1, a+G),(a*g+g, -1, a+G),(a*g+g, 1, -a-G),(a*g+g, -1, -a-G),
            (-a*g-g, 1, a+G),(-a*g-g, -1, a+G),(-a*g-g, 1, -a-G),(-a*g-g, -1, -a-G),
            (a+G, a*g+g, 1),(a+G, -a*g-g, 1),(a+G, a*g+g, -1),(a+G, -a*g-g, -1),
            (-a-G, a*g+g, 1),(-a-G, -a*g-g, 1),(-a-G, a*g+g, -1),(-a-G, -a*g-g, -1)]

#merge identical points together
def mergepoints(points):
    threshold = 1e-5 #maximum distance to merge
    
    newpoints = []
    for p in points:
        if all(abs(p[0]-q[0])+abs(p[1]-q[1])+abs(p[2]-q[2]) > threshold for q in newpoints):
            newpoints.append(p)
    return newpoints