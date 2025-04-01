from multiprocessing import Pool
from multiprocessing.pool import ThreadPool
from pathlib import Path

from tqdm import tqdm

from .check import check_ann_file, check_img
from .utils import get_max_processes, im2txt


class Yoco:
    def __init__(
        self, num_classes: int, ann_folder: str = "labels", num_processes=None
    ):
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

    def validate_list(
        self, ims_list: Path, parallel: bool = False, threading: bool = False
    ):
        with ims_list.open("r") as f:
            ims = f.readlines()

        bad_ims = []
        good_ims = []

        if parallel:
            mpool = ThreadPool if threading else Pool
            with mpool(processes=self.num_processes) as pool:
                results = list(tqdm(pool.imap(self.validate_im, ims), total=len(ims)))

            for i, res in enumerate(results):
                if res:
                    good_ims.append(ims[i])
                else:
                    bad_ims.append(ims[i])

        else:
            for im in tqdm(ims):
                if self.validate_im(im):
                    good_ims.append(im)
                else:
                    bad_ims.append(im)

        return good_ims, bad_ims
