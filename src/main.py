import os
import shutil

DIR_PATH_STATIC = "./static"
DIR_PATH_PUBLIC = "./public"

def main():
    if os.path.exists(DIR_PATH_PUBLIC):
        print(f"Deleting public directory...")
        shutil.rmtree(DIR_PATH_PUBLIC)
    print("Copying static files to public directory...")
    copy_dir_to_dir(DIR_PATH_STATIC, DIR_PATH_PUBLIC)
    return

def copy_dir_to_dir(src: str, dest: str):
    if not os.path.exists(dest):
        os.mkdir(dest)

    for child in os.listdir(src):
        path = os.path.join(src, child)
        dest_path = os.path.join(dest, child)
        print(f"Copying {path} to {dest_path}")
        if os.path.isfile(path):
            shutil.copy(path, dest_path)
        else:
            copy_dir_to_dir(path, dest_path)

if __name__ == "__main__":
    main()