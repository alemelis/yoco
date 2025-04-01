import sys
from yoco import yoco

list_file = sys.argv[1]
yoco.validate_list(list_file, 32)
