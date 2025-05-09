import os
import shutil

def copy_recursive(src, dest):
    # Step 1: If dest exists, clear it entirely
    if os.path.exists(dest):
        shutil.rmtree(dest)
        print(f"Deleted existing contents of: {dest}")

    # Step 2: Recreate the destination directory
    os.makedirs(dest)
    print(f"Created destination directory: {dest}")

    # Step 3: Walk through all items in source
    for item in os.listdir(src):
        s_item = os.path.join(src, item)
        d_item = os.path.join(dest, item)

        if os.path.isdir(s_item):
            # Recurse into subdirectories
            copy_recursive(s_item, d_item)
        else:
            # Copy file and log the path
            shutil.copy2(s_item, d_item)
            print(f"Copied file: {s_item} -> {d_item}")


def read_file(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def write_file(path, content):
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
