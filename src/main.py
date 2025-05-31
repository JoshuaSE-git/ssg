import os
import shutil

from gen_utils import *

DIR_PATH_STATIC = "./static"
DIR_PATH_PUBLIC = "./public"
DIR_PATH_CONTENT = "./content"
TEMPLATE_PATH = "./template.html"

def main():
    if os.path.exists(DIR_PATH_PUBLIC):
        print(f"Deleting public directory...")
        shutil.rmtree(DIR_PATH_PUBLIC)
    print("Copying static files to public directory...")
    copy_dir_to_dir(DIR_PATH_STATIC, DIR_PATH_PUBLIC)

    generate_pages_recursive(DIR_PATH_CONTENT, TEMPLATE_PATH, DIR_PATH_PUBLIC)
    return

if __name__ == "__main__":
    main()