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
    next_alive, _, _ = next_generation(alive)
    assert next_alive == set()


def test_square_is_stable():
    """2x2 square should remain stable"""
    alive = {(5, 5), (6, 5), (5, 6), (6, 6)}
    next_alive, _, _ = next_generation(alive)
    assert next_alive == alive


def test_square_cell_birth():
    """2x2 square should remain stable"""
    alive = {(6, 5), (5, 6), (6, 6)}
    next_alive, _, _ = next_generation(alive)
    assert next_alive == {(5, 5), (6, 5), (5, 6), (6, 6)}


def test_highlife_birth_on_six_neighbors():
    """HighLife (B36/S23) : une cellule morte avec 6 voisins vivants naît,
    ce qui ne se produit pas avec les règles par défaut B3/S23."""
    dead_cell = (0, 0)
    alive = {
        (-1, -1),
        (0, -1),
        (-1, 0),
        (1, 0),
        (-1, 1),
        (0, 1),
    }
    neighbors = get_neighbors(dead_cell)
    live_neighbor_count = sum(1 for n in neighbors if n in alive)
    assert live_neighbor_count == 6

    highlife_alive, _, _ = next_generation(alive, birth={3, 6}, survive={2, 3})
    assert dead_cell in highlife_alive

    default_alive, _, _ = next_generation(alive)
    assert dead_cell not in default_alive
