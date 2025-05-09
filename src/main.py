import os
import shutil

from markdown_parser import generate_pages_recursive

PUBLIC_DIR = "public"
STATIC_DIR = "static"
CONTENT_FILE = "content/index.md"
TEMPLATE_FILE = "template.html"
OUTPUT_FILE = os.path.join(PUBLIC_DIR, "index.html")

def delete_public_dir():
    if os.path.exists(PUBLIC_DIR):
        shutil.rmtree(PUBLIC_DIR)
        print(f"Deleted '{PUBLIC_DIR}' directory.")

def copy_static_to_public():
    shutil.copytree(STATIC_DIR, PUBLIC_DIR)
    print(f"Copied static files from '{STATIC_DIR}' to '{PUBLIC_DIR}'.")

def main():
    delete_public_dir()
    copy_static_to_public()
    generate_pages_recursive("content", "template.html", "public")

if __name__ == "__main__":
    main()
