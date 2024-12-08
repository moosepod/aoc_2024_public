type Point = tuple[int,int]
type Size = tuple[int,int]

type Rect = tuple[Point,Size]

type Grid = dict[Point,str]

type SizedGrid = tuple[Grid,Size]

###
### Constants
###

# Keys for point/size/rect tuples
WIDTH = 0
HEIGHT = 1
X = 0
Y = 1

DIRECTIONS = {
    "NE": (1,-1), 
    "E": (1,0), 
    "SE": (1,1), 
    "S": (0,1), 
    "SW": (-1,1), 
    "W": (-1,0), 
    "NW": (-1,-1), 
    "N": (0,-1), 
    }

###
### Loading puzzle data
###
def load_s(puzzle_number: int, filename: str) -> str:
    with open(f"day_{puzzle_number}/{filename}") as f:
        return f.read()

def load_grid(puzzle_number: int, filename: str) -> SizedGrid:
    g = {}
    width = 0
    height = 0
    with open(f"day_{puzzle_number}/{filename}") as f:
        s = f.read()
        for y, row in enumerate(s.split("\n")):
            if row:
                height += 1
                for x, c in enumerate(row):
                    g[(x,y)] = c
                    if x > width:
                        width = x
    return g, (width+1,height)

###
### POINTS
###
def padd(p1: Point, p2: Point) -> Point:
    return (p1[0] + p2[0], p1[1] + p2[1])

def pmult(p: Point, n: int) -> Point:
    return (p[0] * n, p[1] * n)

def p_in_rect(p: Point, r: Rect):
    return p[0] >= r[0][0] and p[1] >= r[0][1] and p[0] < r[0][0] + r[1][0] and p[1] < r[0][1] + r[1][1]

###
### GRIDS
###

def dump_grid(grid: Grid, size: Size, message: str) -> str:
    s = message
    for row in range(0,size[1]):
        s+="\n"
        for col in range(0,size[1]):
            s+=grid[(col,row)]
    return s
