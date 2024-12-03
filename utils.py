def load_s(puzzle_number: int, filename: str) -> str:
    with open(f"day_{puzzle_number}/{filename}") as f:
        return f.read()
