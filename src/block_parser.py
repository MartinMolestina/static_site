import re
from enum import Enum

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def markdown_to_blocks(markdown):
    # Split on double newlines to get block candidates
    raw_blocks = markdown.strip().split("\n\n")

    blocks = []
    for block in raw_blocks:
        # Clean up whitespace and skip empty blocks
        cleaned_lines = [line.strip() for line in block.strip().splitlines() if line.strip()]
        if not cleaned_lines:
            continue
        # Rejoin cleaned lines with a newline to preserve multi-line blocks
        cleaned_block = "\n".join(cleaned_lines)
        blocks.append(cleaned_block)

    return blocks


        
def block_to_block_type(block: str) -> BlockType:
    lines = block.split("\n")

    # Check for code block
    if block.startswith("```") and block.endswith("```"):
        return BlockType.CODE

    # Check for heading (1-6 # characters followed by a space)
    if re.match(r"^#{1,6} ", lines[0]):
        return BlockType.HEADING

    # Check for quote block: every line starts with >
    if all(line.startswith(">") for line in lines):
        return BlockType.QUOTE

    # Check for unordered list: every line starts with "- "
    if all(line.startswith("- ") for line in lines):
        return BlockType.UNORDERED_LIST

    # Check for ordered list: lines start with 1. 2. 3. etc.
    ordered_match = True
    for i, line in enumerate(lines):
        expected_prefix = f"{i+1}. "
        if not line.startswith(expected_prefix):
            ordered_match = False
            break
    if ordered_match:
        return BlockType.ORDERED_LIST

    # Default: paragraph
    return BlockType.PARAGRAPH



def markdown_to_html_node(markdown: str) -> HTMLNode:
    from block_parser import split_blocks, block_to_block_type
    from inline_parser import text_to_children
    from htmlnode import HTMLNode, TextNode, text_node_to_html_node

    blocks = split_blocks(markdown)
    children = []

    for block in blocks:
        block_type = block_to_block_type(block)

        if block_type == "heading":
            level = len(block) - len(block.lstrip("#"))
            tag = f"h{level}"
            text = block.lstrip("#").strip()
            node = HTMLNode(tag, children=text_to_children(text))

        elif block_type == "paragraph":
            node = HTMLNode("p", children=text_to_children(block.strip()))

        elif block_type == "code":
            code_content = block.strip("```").strip()
            text_node = TextNode(code_content, "text")
            node = HTMLNode("pre", children=[
                HTMLNode("code", children=[text_node_to_html_node(text_node)])
            ])

        elif block_type == "unordered_list":
            items = [line.lstrip("-* ").strip() for line in block.strip().splitlines()]
            li_nodes = [HTMLNode("li", children=text_to_children(item)) for item in items]
            node = HTMLNode("ul", children=li_nodes)

        elif block_type == "ordered_list":
            items = [line.lstrip("0123456789. ").strip() for line in block.strip().splitlines()]
            li_nodes = [HTMLNode("li", children=text_to_children(item)) for item in items]
            node = HTMLNode("ol", children=li_nodes)

        elif block_type == "quote":
            quote_lines = [line.lstrip("> ").strip() for line in block.strip().splitlines()]
            quote_text = "\n".join(quote_lines)
            node = HTMLNode("blockquote", children=text_to_children(quote_text))

        else:
            # Fallback to plain paragraph
            node = HTMLNode("p", children=text_to_children(block.strip()))

        children.append(node)

    return HTMLNode("div", children=children)



