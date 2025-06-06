
import os
import shutil
import sys

from markdown_parser import generate_pages_recursive

# Use 'docs' instead of 'public'
OUTPUT_DIR = "docs"
STATIC_DIR = "static"
CONTENT_DIR = "content"
TEMPLATE_FILE = "template.html"

def delete_output_dir():
    if os.path.exists(OUTPUT_DIR):
        shutil.rmtree(OUTPUT_DIR)
        print(f"Deleted '{OUTPUT_DIR}' directory.")

def copy_static_to_output():
    shutil.copytree(STATIC_DIR, OUTPUT_DIR)
    print(f"Copied static files from '{STATIC_DIR}' to '{OUTPUT_DIR}'.")

def main():
    # Get base path from CLI args, default to "/"
    base_path = sys.argv[1] if len(sys.argv) > 1 else "/"

    delete_output_dir()
    copy_static_to_output()
    generate_pages_recursive(CONTENT_DIR, TEMPLATE_FILE, OUTPUT_DIR, base_path)

if __name__ == "__main__":
    main()

