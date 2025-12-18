from project import create_square_centers, index_to_coord, get_base_coordinates


def test_create_square_centers():
    # Test default grid (15x15)
    centers = create_square_centers()
    assert len(centers) == 225

    # Test a smaller custom grid (2x2)
    # With cell_w=40, cell_h=40, left=0, top=-40:
    # Row 0: cy = -40 + 0*40 + 40 + 20 = 20
    # Col 0: cx = 0 + 0*40 + 20 = 20
    small_centers = create_square_centers(columns=2, rows=2, left=0, top=-40, cell_w=40, cell_h=40)
    assert len(small_centers) == 4
    assert small_centers[0] == (20, 20)


def test_index_to_coord():
    # Test index 0 in default 15x15 grid
    # row = 0 // 15 = 0, col = 0 % 15 = 0
    # x = 0 * 40 + 20 = 20, y = 0 * 40 + 20 = 20
    assert index_to_coord(0) == (20, 20)

    # Test index 15 (first cell of second row)
    # row = 15 // 15 = 1, col = 15 % 15 = 0
    # x = 0 * 40 + 20 = 20, y = 1 * 40 + 20 = 60
    assert index_to_coord(15) == (20, 60)


def test_get_base_coordinates():
    # Test valid colors
    assert get_base_coordinates("red") == [(4, 4), (5, 4), (4, 5), (5, 5)]
    assert get_base_coordinates("blue") == [(9, 9), (10, 9), (9, 10), (10, 10)]

    # Test case sensitivity/invalid color
    assert get_base_coordinates("RED") == []  # Dictionary uses lowercase keys
    assert get_base_coordinates("purple") == []