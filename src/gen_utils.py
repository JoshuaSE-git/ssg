import os
import shutil

from node_utils import *

DIR_PATH_STATIC = "./static"
DIR_PATH_PUBLIC = "./public"
DIR_PATH_CONTENT = "./content"
TEMPLATE_PATH = "./template.html"

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

def extract_title(md: str) -> str:
    h1 = list(filter(lambda x: x.startswith("# "), markdown_to_blocks(md)))
    if len(h1) < 1:
        raise Exception("No title found")
    return h1[0].lstrip("# ")

def generate_page(from_path: str, template_path: str, dest_path: str, base_path: str):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path) as f:
        md = f.read()
    with open(template_path) as f:
        template = f.read()
    title = extract_title(md)
    html_str = markdown_to_html_node(md).to_html()

    template = template.replace("{{ Title }}", title)
    template = template.replace("{{ Content }}", html_str)
    template = template.replace('href="/', f'href="{base_path}')
    template = template.replace('src="/', f'src="{base_path}')

    dest_parent = os.path.dirname(dest_path)
    if not os.path.exists(dest_parent):
        os.makedirs(dest_parent, exist_ok=True)
    with open(dest_path, "w") as f:
        f.write(template)

def generate_pages_recursive(dir_path_content: str, template_path: str, dest_dir_path: str, base_path: str):
    for child in os.listdir(dir_path_content):
        content_path = os.path.join(dir_path_content, child)
        if os.path.isfile(content_path) and child[-3:] == ".md":
            dest_path = os.path.join(dest_dir_path, child[:-3] + ".html")
            generate_page(content_path, template_path, dest_path, base_path)
        else:
            dest_path = os.path.join(dest_dir_path, child)
            generate_pages_recursive(content_path, template_path, dest_path, base_path)









