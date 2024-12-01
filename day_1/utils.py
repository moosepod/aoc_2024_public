def load(name):
    import re
    rx = re.compile(r'^(\d+) +(\d+)$')
    
    l1 = []
    l2 = []

    with open(f"day_1/{name}") as f:
        for line in f.read().split("\n"):
            if line:
                m = rx.search(line)
                s1,s2 = m.group(1), m.group(2)
                l1.append(int(s1))
                l2.append(int(s2))

    return l1,l2
