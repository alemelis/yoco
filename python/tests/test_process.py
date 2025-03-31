from pathlib import Path

import pytest

import yoco


def test_im2txt():
    im = Path("path/to/images/image.jpg")
    ann_folder = "annotations"
    txt_path = yoco.process.im2txt(im, ann_folder)
    assert txt_path == Path("path/to/annotations/image.txt")
