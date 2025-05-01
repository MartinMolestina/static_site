import unittest
from block_parser import markdown_to_blocks

class TestBlockParser(unittest.TestCase):

    def test_markdown_to_blocks(self):
        md = """
    This is **bolded** paragraph

    This is another paragraph with _italic_ text and `code` here
    This is the same paragraph on a new line

    - This is a list
    - with items
    """
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_blocks_strip_whitespace(self):
        md = "   \n\n  This is text  \n\n\n   Another one  \n\n   "
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            ["This is text", "Another one"]
        )

    def test_blocks_single_paragraph(self):
        md = "Just a single paragraph"
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["Just a single paragraph"])

    def test_blocks_heading_and_paragraph(self):
        md = "# Heading\n\nSome paragraph text."
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["# Heading", "Some paragraph text."])

    def test_blocks_multiple_blank_lines(self):
        md = "First block\n\n\n\n\nSecond block"
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["First block", "Second block"])

    def test_blocks_empty_input(self):
        md = "   \n   \n"
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, [])

