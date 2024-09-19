def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    true_blocks = []
    for block in blocks:
        if block == "":
            continue
        true_blocks.append(block.strip())
    return true_blocks