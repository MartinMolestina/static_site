import re
from textnode import TextNode, TextType

def extract_markdown_images(text):
    pattern = r"!\[\s*([^\]]*?)\s*\]\s*\(\s*([^)]+?)\s*\)"
    return re.findall(pattern, text)

def extract_markdown_links(text):
    pattern = r"(?<!!)\[\s*([^\]]*?)\s*\]\s*\(\s*([^)]+?)\s*\)"
    return re.findall(pattern, text)

def split_nodes_link(old_nodes):
    new_nodes = []
    link_pattern = r"(?<!!)\[\s*([^\]]*?)\s*\]\s*\(\s*([^)]+?)\s*\)"

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        text = node.text
        last_index = 0
        for match in re.finditer(link_pattern, text):
            start, end = match.span()
            anchor_text, url = match.groups()

            if start > last_index:
                new_nodes.append(TextNode(text[last_index:start], TextType.TEXT))

            new_nodes.append(TextNode(anchor_text, TextType.LINK, url))
            last_index = end

        if last_index < len(text):
            new_nodes.append(TextNode(text[last_index:], TextType.TEXT))

    return new_nodes


def split_nodes_image(old_nodes):
    new_nodes = []
    image_pattern = r"!\[\s*([^\]]*?)\s*\]\s*\(\s*([^)]+?)\s*\)"

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        text = node.text
        last_index = 0
        for match in re.finditer(image_pattern, text):
            start, end = match.span()
            alt_text, url = match.groups()

            if start > last_index:
                new_nodes.append(TextNode(text[last_index:start], TextType.TEXT))

            new_nodes.append(TextNode(alt_text, TextType.IMAGE, url))
            last_index = end

        if last_index < len(text):
            new_nodes.append(TextNode(text[last_index:], TextType.TEXT))

    return new_nodes
