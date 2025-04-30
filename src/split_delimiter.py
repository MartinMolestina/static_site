from textnode import TextType, TextNode

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            # Leave non-text nodes unchanged
            new_nodes.append(node)
            continue

        # Split by delimiter
        parts = node.text.split(delimiter)

        # If there's an even number of parts, assume unmatched delimiters: treat entire text as plain
        if len(parts) % 2 == 0:
            new_nodes.append(node)
            continue

        for i, part in enumerate(parts):
            if part == "":
                continue  # Skip empty strings from split
            if i % 2 == 0:
                # Even index -> normal text
                new_nodes.append(TextNode(part, TextType.TEXT))
            else:
                # Odd index -> inside delimiter
                new_nodes.append(TextNode(part, text_type))

    return new_nodes
