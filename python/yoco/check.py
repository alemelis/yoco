from pathlib import Path

from PIL import Image


def check_img(im_path: Path) -> bool:
    with Image.open(im_path) as img:
        try:
            img.verify()
            return True
        except Exception:
            return False


def check_ann(ann: str, num_classes: int) -> bool:
    if not ann:
        return True

    data = ann.split()
    if len(data) != 5:
        return False

    c, *coords = data
    try:
        c = int(c)
        x, y, w, h = list(map(float, coords))
    except ValueError:
        return False

    if c < 0 or c >= num_classes:
        return False

    if x < 0.0 or x > 1.0:
        return False

    if y < 0.0 or y > 1.0:
        return False

    if w <= 0.0 or w > 1.0:
        return False

    if h <= 0.0 or h > 1.0:
        return False

    if x + w > 1.0 or y + h > 1.0:
        return False

    return True


def check_ann_file(p: Path, num_classes: int) -> bool:
    with p.open("r") as f:
        lines = f.readlines()

    if not lines:
        return True

    for line in lines:
        if not check_ann(line.strip(), num_classes):
            return False

    return True
