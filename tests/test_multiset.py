from eggmt.multiset import *


def test_overlap():
    assert list(overlap([("a", 1), ("b", 2)], [("a", 1), ("c", 3)])) == [
        ("a", 1),
        ("b", 2),
        ("c", 3),
    ]
    assert overlap([("a", 1), ("b", 2)], [("c", 1)]) is None


def test_sub():
    assert sub([("a", 1), ("b", 2)], [("a", 1), ("c", 3)]) is None
    assert sub([("a", 1), ("b", 2)], [("a", 1), ("b", 2)]) == []


def test_add():
    assert list(add([("a", 1), ("b", 2)], [("a", 1), ("c", 3)])) == [
        ("a", 2),
        ("b", 2),
        ("c", 3),
    ]


def test_replace():
    assert replace([("a", 1), ("b", 2)], [("a", 1)], [("a", 2), ("c", 3)]) == [
        ("a", 2),
        ("b", 2),
        ("c", 3),
    ]
    assert replace(
        [("a", 1), ("b", 2)], [("a", 1), ("b", 2)], [("a", 2), ("c", 3)]
    ) == [("a", 2), ("c", 3)]
    assert replace([("a", 1), ("b", 2)], [("a", 1), ("b", 4)], [("a", 2)]) == None
    assert replace([("p", 25)], [("p", 25)], [("q", 1)]) == [("q", 1)]
