#Game of life rules
#Any live cell with fewer than two live neighbours dies, as if by underpopulation.
#Any live cell with two or three live neighbours lives on to the next generation.
#Any live cell with more than three live neighbours dies, as if by overpopulation.
#Any dead cell with exactly three live neighbours becomes a live cell, as if by reproduction

from typing import Generator


NEIGHBORS = [
    (-1, -1), (0, -1), (1, -1),
    (-1,  0),          (1,  0),
    (-1,  1), (0,  1), (1,  1)
]

def get_neighbors(cell) -> set[tuple[int]]:
    return set([(cell[0] + dx, cell[1] + dy) for dx, dy in NEIGHBORS])

def next_generation(alive: set) -> tuple[set[tuple[int]], set[tuple[int]], set[tuple[int]]]:
    """
    alive : set([tuple, tuple]) - liste des cellules vivantes
    on recupere la liste des voisins de chaque cellules vivantes
    on va ensuite regarder le nombre de voisins de chaque cellule récupéré   
    """
    relevant_cells = set()
    next_alive = set()
    born_cells = set()
    dead_cells = set()
    
    for cell in alive:
        relevant_cells.add(cell)
        relevant_cells.update(get_neighbors(cell))
    
    for cell in relevant_cells:
        neighbors  = get_neighbors(cell)
        count = sum(1 for n in neighbors if n in alive)
        if cell in alive:
            if count in [2, 3]:
                next_alive.add(cell)  
        else:
            if count == 3:
                born_cells.add(cell)
                next_alive.add(cell)        
    dead_cells = alive - next_alive
    return next_alive, born_cells, dead_cells
    
    
    
    