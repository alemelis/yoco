import pytest

import yoco


def test_check_ann():
    num_classes = 5
    assert yoco.check_ann("", num_classes)
    assert not yoco.check_ann(" ", num_classes)

    assert not yoco.check_ann("1 0.0 0.0 0.1", num_classes)
    assert not yoco.check_ann("1 0.0 0.0 0.1 0.1 a", num_classes)

    assert not yoco.check_ann("1.0 0.0 0.0 0.1 0.1", num_classes)
    assert not yoco.check_ann("6 0.0 0.0 0.1 0.1", num_classes)
    assert not yoco.check_ann("-1 0.0 0.0 0.1 0.1", num_classes)

    assert not yoco.check_ann("1 -0.1 0.0 0.1 0.1", num_classes)
    assert not yoco.check_ann("1 1.0 0.0 0.1 0.1", num_classes)
    assert not yoco.check_ann("1 0.0 -0.1 0.1 0.1", num_classes)
    assert not yoco.check_ann("1 0.0 1.0 0.1 0.1", num_classes)
    assert not yoco.check_ann("1 0.0 0.0 1.1 0.1", num_classes)
    assert not yoco.check_ann("1 0.0 0.0 0.0 0.1", num_classes)
    assert not yoco.check_ann("1 0.0 0.0 0.1 1.1", num_classes)
    assert not yoco.check_ann("1 0.0 0.0 0.1 0.0", num_classes)
    assert not yoco.check_ann("1 0.5 0.5 0.1 0.6", num_classes)

    assert yoco.check_ann("1 0.1 0.2 0.3 0.4", num_classes)


def test_check_ann_file():
    num_classes = 5
    assert yoco.check_ann_file("src/tests/assets/valid.txt", num_classes)
    assert not yoco.check_ann_file("src/tests/assets/invalid.txt", num_classes)
