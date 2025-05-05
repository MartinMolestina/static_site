import unittest
from block_parser import markdown_to_blocks, block_to_block_type, BlockType

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



class TestBlockToBlockType(unittest.TestCase):

    def test_heading_block(self):
        self.assertEqual(block_to_block_type("# Heading"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("###### Subheading"), BlockType.HEADING)

    def test_code_block(self):
        code = "```\ndef func():\n    pass\n```"
        self.assertEqual(block_to_block_type(code), BlockType.CODE)

    def test_quote_block(self):
        quote = "> This is a quote\n> With another line"
        self.assertEqual(block_to_block_type(quote), BlockType.QUOTE)

    def test_unordered_list_block(self):
        ul = "- First item\n- Second item"
        self.assertEqual(block_to_block_type(ul), BlockType.UNORDERED_LIST)

    def test_ordered_list_block(self):
        ol = "1. First item\n2. Second item\n3. Third item"
        self.assertEqual(block_to_block_type(ol), BlockType.ORDERED_LIST)

    def test_paragraph_block(self):
        paragraph = "This is just a normal paragraph of text.\nIt goes on a second line."
        self.assertEqual(block_to_block_type(paragraph), BlockType.PARAGRAPH)

    def test_invalid_heading(self):
        self.assertEqual(block_to_block_type("####### Not a valid heading"), BlockType.PARAGRAPH)

    def test_mixed_quote_and_text(self):
        mixed = "> Quote line\nNormal line"
        self.assertEqual(block_to_block_type(mixed), BlockType.PARAGRAPH)

    def test_unordered_list_with_extra_space(self):
        invalid_ul = "-item without space\n- second item"
        self.assertEqual(block_to_block_type(invalid_ul), BlockType.PARAGRAPH)

    def test_ordered_list_wrong_start(self):
        wrong_ol = "0. First\n1. Second"
        self.assertEqual(block_to_block_type(wrong_ol), BlockType.PARAGRAPH)

    def test_ordered_list_wrong_increment(self):
        bad_ol = "1. First\n3. Second"
        self.assertEqual(block_to_block_type(bad_ol), BlockType.PARAGRAPH)


if __name__ == '__main__':
    unittest.main()
