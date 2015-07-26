from csp import *
from utils import *
from csp_search import *
from types import *
# Kakuro Problem

class kakuro(CSP):
    """ 
    >>> backtracking_search(australia)
    {'WA': 'R', 'Q': 'R', 'T': 'R', 'V': 'R', 'SA': 'G', 'NT': 'B', 'NSW': 'B'}
    >>> backtracking_search(australia, select_unassigned_variable=mrv)
    {'WA': 'R', 'Q': 'R', 'T': 'R', 'V': 'R', 'SA': 'G', 'NT': 'B', 'NSW': 'B'}
    >>> backtracking_search(australia, inference=forward_checking)
    {'Q': 'R', 'T': 'R', 'WA': 'R', 'V': 'R', 'SA': 'G', 'NT': 'B', 'NSW': 'B'}
    >>> backtracking_search(australia, inference=mac)
    {'WA': 'R', 'Q': 'R', 'T': 'R', 'V': 'R', 'SA': 'G', 'NT': 'B', 'NSW': 'B'}
    >>> backtracking_search(usa, select_unassigned_variable=mrv, inference=mac)
    {'WA': 'R', 'DE': 'G', 'DC': 'R', 'WI': 'G', 'WV': 'B', 'HI': 'R', 'FL': 'B', 'WY': 'R', 'NH': 'G', 'NJ': 'B', 'NM': 'R', 'TX': 'G', 'LA': 'B', 'NC': 'R', 'ND': 'R', 'NE': 'B', 'TN': 'B', 'NY': 'G', 'PA': 'R', 'RI': 'G', 'NV': 'R', 'VA': 'G', 'CO': 'G', 'CA': 'G', 'AL': 'R', 'AR': 'R', 'VT': 'R', 'IL': 'B', 'GA': 'G', 'IN': 'G', 'IA': 'R', 'MA': 'B', 'AZ': 'B', 'ID': 'G', 'CT': 'R', 'ME': 'R', 'MD': 'Y', 'KA': 'R', 'OK': 'B', 'OH': 'Y', 'UT': 'Y', 'MO': 'G', 'MN': 'B', 'MI': 'R', 'AK': 'R', 'MT': 'B', 'MS': 'G', 'SC': 'B', 'KY': 'R', 'OR': 'B', 'SD': 'G'}
    >>> min_conflicts(usa, 100000)
    {'WA': 'R', 'DE': 'G', 'DC': 'R', 'WI': 'G', 'WV': 'B', 'HI': 'R', 'FL': 'B', 'WY': 'R', 'NH': 'G', 'NJ': 'B', 'NM': 'R', 'TX': 'G', 'LA': 'B', 'NC': 'R', 'ND': 'R', 'NE': 'B', 'TN': 'B', 'NY': 'G', 'PA': 'R', 'RI': 'G', 'NV': 'R', 'VA': 'G', 'CO': 'G', 'CA': 'G', 'AL': 'R', 'AR': 'R', 'VT': 'R', 'IL': 'B', 'GA': 'G', 'IN': 'G', 'IA': 'R', 'OK': 'B', 'AZ': 'B', 'ID': 'G', 'CT': 'R', 'ME': 'R', 'MD': 'Y', 'KA': 'R', 'MA': 'B', 'OH': 'Y', 'UT': 'Y', 'MO': 'G', 'MN': 'B', 'MI': 'R', 'AK': 'R', 'MT': 'B', 'MS': 'G', 'SC': 'B', 'KY': 'R', 'OR': 'B', 'SD': 'G'}
    """

    def __init__(self, colors, neighbors):
        """Make a CSP for the problem of coloring a map with different colors
        for any two adjacent regions.  Arguments are a list of colors, and a
        dict of {region: [neighbor,...]} entries.  This dict may also be
        specified as a string of the form defined by parse_neighbors."""
        
        if isinstance(neighbors, str):
            neighbors = parse_neighbors(neighbors)
        domain=dict()    
        for i in neighbors.keys():
            domain[i]=colors
                
        CSP.__init__(self, neighbors.keys(), domain, neighbors, self.has_conflict)        
                   
    def has_conflict(self, var, val, assignment):
        "A constraint saying two neighboring variables must differ in value."
        x=len(self.neighbors[var][1]); """geitones ston xx'"""
        y=len(self.neighbors[var][2]);"""geitones ston yy'"""
        #print('ARXH THS HAS CONFLICT')
        for i in range(x):
            if(assignment.get(self.neighbors[var][1][i])==val):
                return True
        for i in range(y):
            if(assignment.get(self.neighbors[var][2][i])==val):
                return True

        if int(val)>=self.neighbors[var][0][0] or int(val)>=self.neighbors[var][0][1]:
            return True
        n=len(self.neighbors.keys())-1

        cu=0
        a8=0
        """elegxw an oloi oi suggeneis exoun timh k koitaw a8roisma"""
        for i in range(len(self.neighbors[var][1])):
            if(assignment.get(self.neighbors[var][1][i]))== None:
                cu=2
                break
        if(cu!=2):
            for i in range (len(self.neighbors[var][1])):
                a8+=int(assignment[self.neighbors[var][1][i]])
            a8+=int(val)
            if(a8- self.neighbors[var][0][0]!=0):
                return True
        cu=0
        a8=0
        for i in range(len(self.neighbors[var][2])):
            
            if(assignment.get(self.neighbors[var][2][i]))== None:
                cu=2
                break
        if(cu!=2):
            for i in range (len(self.neighbors[var][2])):
                a8+=int(assignment[self.neighbors[var][2][i]])
            a8+=int(val)
            if(a8- self.neighbors[var][0][1]!=0):
                return True
       # print(' var val')
       # print(var);print(val);print('--------')
        return False


def parse_neighbors(neighbors, vars=[]):
    """Convert a string of the form 'X: Y Z; Y: Z' into a dict mapping
    regions to neighbors.  The syntax is a region name followed by a ':'
    followed by zero or more region names, followed by ';', repeated for
    each region name.  If you say 'X: Y' you don't need 'Y: X'.
    >>> parse_neighbors('X: Y Z; Y: Z')
    {'Y': ['X', 'Z'], 'X': ['Y', 'Z'], 'Z': ['X', 'Y']}
    """
    dict = DefaultDict([])
    for var in vars:
        dict[var] = []
    specs = [spec.split(':') for spec in neighbors.split(';')]
    for (A, Aneighbors) in specs:
        A = A.strip()
        dict.setdefault(A, [])
        for B in Aneighbors.split():
            dict[A].append(B)
            dict[B].append(A)
    """den exw kanei epanalhptikh diadikasia gia ta le3ika
        vasika..exw kanei mono tous periorismous se has conflict
        kai sthn fc sto csp_search.py alla auto me to fc..petaei sfalma"""
    d={}
    d[0]=([3,10],[1],[2,5])
    d[1]=([3,13],[0],[3,6])
    d[2]=([12,10],[3,4],[0,5])
    d[3]=([12,13],[2,4],[1,6])
    d[4]=([12,13],[2,3],[7])
    d[5]=([21,10],[6,7],[0,2])
    d[6]=([21,13],[5,7],[1,3])
    d[7]=([21,13],[5,6],[4])
    
    return d



puzzle0 = [\
[  '*'  ,  '*'  ,  '*'  ,[ 6,''],[ 3,'']],\
[  '*'  ,[ 4,''],[ 3, 3],  '_'  ,  '_'  ],\
[['',10],  '_'  ,  '_'  ,  '_'  ,  '_'  ],\
[['', 3],  '_'  ,  '_'  ,  '*'  ,  '*'  ]]

puzzle1 = [\
[  '*'  ,[10,''],[13,''],  '*'  ],\
[['', 3],  '_'  ,  '_'  ,[13,'']],\
[['',12],  '_'  ,  '_'  ,  '_'  ],\
[['',21],  '_'  ,  '_'  ,  '_'  ]]

"""
puzzle2
d={}
d[0]=([9,17],[1],[4])
d[1]=([9,28],[0],[5,9,13,17,21,26])
d[2]=([14,42],[3],[7,11,15,19,23,27])
d[3]=([14,22],[2],[8,12])
d[4]=([20,17],[5,6,7,8],[0])
d[5]=([20,28],[4,6,7,8],[1,9,13,17,21,26])
d[6]=([20,31],[4,5,7,8],[10,14,18,22])
d[7]=([20,42],[4,5,6,8],[2,11,15,19,23,27])
d[8]=([20,22],[4,5,6,7],[3,12])
d[9]=([30,28],[10,11,12],[1,5,13,17,21,26])
d[10]=([30,31],[9,11,12],[6,14,18,22])
d[11]=([30,42],[9,10,12],[2,7,15,19,23,27])
d[12]=([30,22],[9,10,11],[3,8])
d[13]=([24,28],[14,15],[1,5,9,17,21,26])
d[14]=([24,31],[13,15],[6,10,18,22])
d[15]=([24,42],[13,14],[2,7,11,19,23,27])
d[16]=([25,22],[17,18,19],[20,25])
d[17]=([25,28],[16,18,19],[1,5,9,13,21,26])
d[18]=([25,31],[16,17,19],[6,10,14,22])
d[19]=([25,42],[16,17,18],[2,7,11,15,23,27])
d[20]=([20,22],[21,22,23,24],[16,25])
d[21]=([20,28],[20,22,23,24],[1,5,9,13,17,26])
d[22]=([20,31],[20,21,23,24],[6,10,14,18])
d[23]=([20,42],[20,21,22,24],[2,7,11,15,19,27])
d[24]=([20,11],[20,21,22,23],[28])
d[25]=([14,22],[26],[16,20])
d[26]=([14,28],[25],[1,5,9,13,17,21])
d[27]=([17,42],[28],[2,7,11,15,19,23])
d[28]=([17,11],[27],[24])
puzzle0
d={} 
d[0]=([3,6],[1],[4])
d[1]=([3,3],[0],[5])
d[2]=([10,4],[3,4,5],[6])
d[3]=([10,3],[2,4,5],[7])
d[4]=([10,6],[2,3,5],[0])
d[5]=([10,3],[2,3,4],[1])
d[6]=([3,4],[7],[2])
d[7]=([3,3],[6],[3])

puzzle1
d={}
d[0]=([3,10],[1],[2,5])
d[1]=([3,13],[0],[3,6])
d[2]=([12,10],[3,4],[0,5])
d[3]=([12,13],[2,4],[1,6])
d[4]=([12,13],[2,3],[7])
d[5]=([21,10],[6,7],[0,2])
d[6]=([21,13],[5,7],[1,3])
d[7]=([21,13],[5,6],[4])
"""

puzzle1 = kakuro(list('123456789'), """SA: WA NT Q NSW V; NT: WA Q; NSW: Q V; T: """)
        

