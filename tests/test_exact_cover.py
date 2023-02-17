from malib import exact_cover


def test_exact_cover():
    piece_to_constraints = {"A": {1}, "B": {2, 4}, "C": {2, 3, 5}, "D": {3, 5}}
    assert list(exact_cover(piece_to_constraints)) == [("A", "B", "D")]
