from eggmt.string_kb import *


def test_string():
    assert subseq((2, 2), (1, 1, 1, 2, 2)) == 3
    assert subseq((2, 2), (1, 1, 1, 2, 2, 2)) == 3
    assert subseq((), (1, 2, 3)) == 0
    assert subseq((3, 4), (4, 5, 3)) is None
    assert subseq((3, 4), (4, 5, 3, 4)) == 2

    assert replace((1, 2, 3, 4), (2, 3), (5, 6)) == (1, 5, 6, 4)
    assert replace((1, 2, 3, 4), (2, 3), (5, 6, 7)) == (1, 5, 6, 7, 4)
    assert replace((1, 2, 3, 4), (2, 3), (5, 6, 7, 8)) == (1, 5, 6, 7, 8, 4)
    assert replace((1, 1), (4, 4), (2, 2)) == (1, 1)

    assert rewrite((1, 2, 3, 4), [((2, 3), (5, 6)), ((5, 6), (7, 8))]) == (1, 7, 8, 4)
    assert rewrite((1, 1, 1, 1, 1, 1), [((1, 1), ())]) == ()
    assert rewrite((1, 1, 1, 1, 2, 1), [((1, 1), ())]) == (2, 1)

    assert set(overlaps((1, 2), (2, 3))) == {(1, 2, 3)}
    assert set(overlaps((1, 2), (3, 2))) == set()
    assert set(overlaps((1, 2), (2, 1))) == {(1, 2, 1), (2, 1, 2)}
    assert set(overlaps((1, 2), (1, 2))) == {(1, 2)}
    assert set(overlaps((2, 2), (2, 2, 3))) == {(2, 2, 3), (2, 2, 2, 3)}
    assert set(overlaps((), (1, 2))) == {(1, 2)}  # Hmm. Kind of a weird edge case

    e = 0
    a = 1  # a is rottate square
    b = 2  # b is flip square horizontally.
    E = [
        ((-a, a), ()),  # inverse -b * b = 1
        ((-b, b), ()),  # inverse -a * a = 1
        ((a, a, a, a), ()),  # a^4 = 1
        ((b, b), ()),  # b^2 = 1
        ((a, a, a, b), (b, a)),  # a^3 b = ba
    ]
    print(E)
    print(KB(E))
