import pytest

import yoco


def test_sum_as_string():
    assert yoco.sum_as_string(1, 1) == "2"
