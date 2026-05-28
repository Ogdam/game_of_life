from engine.rules import get_neighbors, next_generation

def test_get_neighbors():
    """Test that get_neighbors returns 8 surrounding cells"""
    cell = (1, 1)
    neighbors = get_neighbors(cell)
    assert len(neighbors) == 8
    assert (0, 0) in neighbors
    assert (2, 2) in neighbors

def test_single_cell_dies():
    """A single live cell with no neighbors dies"""
    alive = {(5, 5)}
    result = next_generation(alive)
    assert result == set()

def test_square_is_stable():
    """2x2 square should remain stable"""
    alive = {(5, 5), (6, 5), (5, 6), (6, 6)}
    result = next_generation(alive)
    assert result == alive
    
def test_square_cell_birth():
    """2x2 square should remain stable"""
    alive = {(6, 5), (5, 6), (6, 6)}
    result = next_generation(alive)
    assert result == {(5,5), (6, 5), (5, 6), (6, 6)}