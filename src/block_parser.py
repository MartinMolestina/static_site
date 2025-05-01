def markdown_to_blocks(markdown):
    # Split on double newlines
    raw_blocks = markdown.split("\n\n")

    blocks = []
    for block in raw_blocks:
        if block.strip() == "":
            continue

        # Clean up each line inside the block
        cleaned_lines = [line.strip() for line in block.strip().split("\n")]
        cleaned_block = "\n".join(cleaned_lines)
        blocks.append(cleaned_block)

    return blocks
