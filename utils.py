type Point = tuple[int,int]
type Size = tuple[int,int]

type Grid = dict[Point,str]

type SizedGrid = tuple[Grid,Size]

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

def padd(p1: tuple[int,int], p2: tuple[int,int]):
    return (p1[0] + p2[0], p1[1] + p2[1])




    
