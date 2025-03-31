from functools import partial
from multiprocessing import Pool
from pathlib import Path

from tqdm import tqdm

from .check import check_ann_file, check_img
from .utils import get_max_processes, im2txt


class Yoco:
    def __init__(self, num_classes: int, ann_folder: str = "labels", num_processes=None):
        self.num_classes = num_classes
        self.ann_folder = ann_folder
        self.num_processes = num_processes or get_max_processes()

    def validate_im(self, line: str) -> bool:
        im = Path(line.strip())
        ann_file = im2txt(im, self.ann_folder)
        if not check_ann_file(ann_file, self.num_classes):
            return False

        if not check_img(im):
            return False

        return True

    def validate_list(self, ims_list: Path):
        with ims_list.open("r") as f:
            ims = f.readlines()

        bad_ims = []
        good_ims = []
        for im in tqdm(ims):
            if not im:
                continue
            if self.validate_im(im):
                good_ims.append(im)
            else:
                bad_ims.append(im)

    def parallel_validate_list(self, ims_list: Path):
        with ims_list.open("r") as f:
            ims = f.readlines()

        bad_ims = []
        good_ims = []

        # Create a partial function with fixed arguments
        process_func = partial(self.validate_im, num_classes=self.num_classes, ann_folder=self.ann_folder)

        # Process images in parallel
        with Pool(processes=self.num_processes) as pool:
            results = list(tqdm(pool.imap(process_func, ims), total=len(ims)))

        # Collect results
        for i, res in enumerate(results):
            if res:
                good_ims.append(ims[i])
            else:
                bad_ims.append(ims[i])
