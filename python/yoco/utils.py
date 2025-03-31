import os
from pathlib import Path


def get_max_processes():
    try:
        return len(os.sched_getaffinity(0))
    except AttributeError:
        # os.sched_getaffinity() is not available on all platforms
        return os.cpu_count() or 1


def im2txt(im: Path, ann_folder: str) -> Path:
    return im.parent.parent / ann_folder / f"{im.stem}.txt"
