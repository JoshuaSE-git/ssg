import os
import shutil
import sys

from gen_utils import *

DIR_PATH_STATIC = "./static"
DIR_PATH_CONTENT = "./content"
DIR_PATH_DOCS = "./docs"
TEMPLATE_PATH = "./template.html"

def main():
    base_path = "/"
    if len(sys.argv) > 1:
        base_path = sys.argv[1]

    if os.path.exists(DIR_PATH_DOCS):
        print(f"Deleting docs directory...")
        shutil.rmtree(DIR_PATH_DOCS)
    print("Copying static files to docs directory...")
    copy_dir_to_dir(DIR_PATH_STATIC, DIR_PATH_DOCS)

    generate_pages_recursive(DIR_PATH_CONTENT, TEMPLATE_PATH, DIR_PATH_DOCS, base_path)
    return

if __name__ == "__main__":
    main()