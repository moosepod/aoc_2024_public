type Point = tuple[int,int]
type PointVector = tuple[Point,Point]
type Size = tuple[int,int]

type Rect = tuple[Point,Size]

type Grid = dict[Point,str]

type SizedGrid = tuple[Grid,Size]

type Line = tuple[Point,Point]

###
### Constants
###

# Keys for point/size/rect tuples
WIDTH = 0
HEIGHT = 1
X = 0
Y = 1
P = 0
V = 1

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

# Cardinal directions and their reverse
NESW = (DIRECTIONS["N"], DIRECTIONS["E"], DIRECTIONS["S"], DIRECTIONS["W"])
SWNE = (DIRECTIONS["S"], DIRECTIONS["W"], DIRECTIONS["N"], DIRECTIONS["E"])

# Misc constant
LABEL_OFFSET = -2

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

def load_grid_int(puzzle_number: int, filename: str) -> SizedGrid:
    grid, size = load_grid(puzzle_number, filename)

    return {p: int(v) if v != '.' else None for p,v in grid.items()}, size

###
### POINTS
###
def padd(p1: Point, p2: Point) -> Point:
    return (p1[X] + p2[X], p1[Y] + p2[Y])

def dot(p1: Point, p2: Point) -> int:
    return p1[0]*p2[0] + p1[1] * p2[1]

def pmult(p: Point, n: int) -> Point:
    return (p[X] * n, p[Y] * n)

def p_in_rect(p: Point, r: Rect):
    return p[X] >= r[P][X] and p[Y] >= r[P][Y] and p[X] < r[P][X] + r[1][WIDTH] and p[1] < r[P][Y] + r[1][HEIGHT]

def padd_mod(p1: Point, p2: Point, size: Size) -> Point:
    x = p1[0] + p2[0]
    y = p1[1] + p2[1]
    if x < 0:
        x = size[WIDTH] + x
    if x >= size[WIDTH]:
        x = x - size[WIDTH] 
    if y < 0:
        y = size[HEIGHT] + y
    if y >= size[HEIGHT]:
        y = y - size[HEIGHT]
        
    return (x,y)

###
### GRIDS
###

def list_to_grid(points: list[Point], c="x") -> Grid:
    return {p: "x" for p in points}

def square_verticies(square: Point) -> list[Point]:
    return [square,
            padd(square,(1,0)),
            padd(square,(1,1)),
            padd(square,(0,1))]

def squares_to_grid(squares: list[Point], c="x") -> Grid:
    """ Convert a list of locations of squares to actual grid points """
    grid = {}

    for p in squares:
        grid[p] = c
        grid[padd(p,(0,1))] = c
        grid[padd(p,(1,0))] = c
        grid[padd(p,(1,1))] = c

    return grid

def dump_grid(grid: Grid, size: Size, message: str="", int_grid=False, extra:dict[Point,str] = None, labels=False) -> str:
    s = message
    for row in range(LABEL_OFFSET if labels else 0,size[1]):
        if s:
            s+="\n"
        for col in range(LABEL_OFFSET if labels else 0,size[0]):
            c = (extra or {}).get((col,row))
            if c is None:
                c = grid.get((col,row))
            if int_grid:
                if c is not None:
                    if c >= 0 and c <= 10:
                        c = chr(48+c)
                    else:
                        c = "?"
            s+=str(c) if c is not None else '.'
    return s

def init_grid(size: Size, cell_size: int, c: str=".", labels = False) -> tuple[Grid,Size]:
    real_size = (size[WIDTH] * cell_size, size[HEIGHT] * cell_size)
    grid = {(x,y): c for x in range(0,real_size[WIDTH]) for y in range(0, real_size[HEIGHT])}

    if labels:
        for x in range(0,size[WIDTH]):
            grid[(x*cell_size, LABEL_OFFSET)] = x % 10
        for y in range(0,size[HEIGHT]):
            grid[(LABEL_OFFSET, y*cell_size)] = y % 10


    
    return grid, real_size

def draw_point(grid: Grid, p: Point, cell_size: int, c:str = "x"):
    grid[pmult(p,cell_size)] = c

def draw_straight_line(grid: Grid, p1: Point, p2: Point, cell_size: int):
    if p1[X] != p2[X] and p1[Y] != p2[Y]:
        raise Exception("Only straight lines supported")        
    
    if p1[Y] < p2[Y]:
        for y in range(p1[Y]*cell_size, p2[Y]*cell_size):
            grid[(p1[X]*cell_size, y)] = "|"
    elif p1[Y] < p2[Y]:
        for y in range(p2[Y]*cell_size, p1[Y]*cell_size):
            grid[(p1[X]*cell_size, y)] = "|"
    elif p1[X] < p2[X]:
        for x in range(p1[X]*cell_size, p2[X]*cell_size):
            grid[(x,p1[Y]*cell_size)] = "-"
    elif p2[X] < p1[X]:
        for x in range(p2[X]*cell_size, p1[X]*cell_size):
            grid[(x,p1[Y]*cell_size)] = "-"


def draw_lines(grid: Grid, cell_size: int, lines: list[Line]):
    for p1, p2 in lines:
        draw_straight_line(grid, p1, p2, cell_size)        

DIRECTION_ARROWS = {(1,0): ">",
                    (-1,0): "<",
                    (0,1): "v",
                    (0,-1): "^"}

def line_direction(line: Line) -> Point:
    p1,p2 = line
    if p1[X] != p2[X] and p1[Y] != p2[Y]:
        raise Exception("Only straight lines supported")        
    if p1[X] < p2[X]:
        return (1,0)
    if p1[X] > p2[X]:
        return (-1,0)
    if p1[Y] < p2[Y]:
        return (0, 1)

    return (0,-1)
    
def draw_arrows(grid: Grid, cell_size: int, lines: list[Line]):
    for p1, p2 in lines:
        draw_straight_line(grid, p1, p2, cell_size)
    for p1, p2 in lines:
        #  Draw @ where lines clash
        if grid.get(pmult(p2,cell_size)) in ('>','<','^','v'):
            c = "@"
        else:
            c = DIRECTION_ARROWS[line_direction((p1,p2))]
        draw_point(grid, p2, cell_size, c)


def draw_verticies(grid: Grid, cell_size: int, region: list[Point]):
    for cell in region:
        for p in square_verticies(cell):
            draw_point(grid, p, cell_size)
