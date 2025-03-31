import pytest

import yoco


def test_good_ann():
    ann = "0 0.1 0.1 0.1 0.1"
    num_classes = 5
    assert yoco.check.check_ann(ann, num_classes)


def test_bad_class():
    num_classes = 5
    for c in [-1, 1.0, 5, 6, "a"]:
        ann = f"{c} 0.1 0.1 0.1 0.1"
        assert not yoco.check.check_ann(ann, num_classes)


def test_bad_xy():
    num_classes = 5
    c = [0.4, -1, -0.1, 1.2, "a"]
    for x in c:
        for y in c:
            if x == y:
                continue
            ann = f"0 {x} {y} 0.1 0.1"
            assert not yoco.check.check_ann(ann, num_classes)


def test_bad_wh():
    num_classes = 5
    c = [0.4, -1, -0.1, 1.2, 0.91, 0.0, "a"]
    for w in c:
        for h in c:
            if w == h:
                continue
            ann = f"0 0.1 0.1 {w} {h}"
            assert not yoco.check.check_ann(ann, num_classes)
