import os

from file_utils import read_file, write_file
from markdown_blocks import markdown_to_html_node

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    # Read files
    markdown = read_file(from_path)
    template = read_file(template_path)

    # Generate HTML content and title
    html_node = markdown_to_html_node(markdown)
    html_content = html_node.to_html()
    title = extract_title(markdown)

    # Fill template
    result = template.replace("{{ Title }}", title)
    result = result.replace("{{ Content }}", html_content)

    # Ensure destination directory exists
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)

    # Write output
    write_file(dest_path, result)


def extract_title(markdown: str) -> str:
    """
    Extracts the first h1 title (line starting with "# ") from the given markdown string.
    Raises a ValueError if no h1 header is found.
    """
    for line in markdown.splitlines():
        line = line.strip()
        if line.startswith("# "):  # Ensure it's a single '#' and a space
            return line[2:].strip()
    raise ValueError("No H1 header found in markdown.")
