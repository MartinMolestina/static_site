import unittest
from textnode import TextNode, TextType, text_node_to_html_node
from split_delimiter import split_nodes_delimiter

class TestTextNode(unittest.TestCase):

    def test_eq(self):
        node1 = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node1, node2)

    def test_not_eq_text(self):
        node1 = TextNode("Hello", TextType.ITALIC)
        node2 = TextNode("Goodbye", TextType.ITALIC)
        self.assertNotEqual(node1, node2)

    def test_not_eq_type(self):
        node1 = TextNode("Some text", TextType.BOLD)
        node2 = TextNode("Some text", TextType.ITALIC)
        self.assertNotEqual(node1, node2)

    def test_not_eq_url(self):
        node1 = TextNode("Click here", TextType.LINK, "https://example.com")
        node2 = TextNode("Click here", TextType.LINK, "https://different.com")
        self.assertNotEqual(node1, node2)

    def test_eq_with_none_url(self):
        node1 = TextNode("Image", TextType.IMAGE)
        node2 = TextNode("Image", TextType.IMAGE, None)
        self.assertEqual(node1, node2)

    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_bold(self):
        node = TextNode("Bold text", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "Bold text")

    def test_italic(self):
        node = TextNode("Italic text", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "Italic text")

    def test_code(self):
        node = TextNode("print('Hello')", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "print('Hello')")

    def test_link(self):
        node = TextNode("Click here", TextType.LINK, url="https://example.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "Click here")
        self.assertEqual(html_node.props, {"href": "https://example.com"})

    def test_image(self):
        node = TextNode("An image", TextType.IMAGE, url="https://example.com/image.png")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props, {"src": "https://example.com/image.png", "alt": "An image"})

    def test_invalid_type(self):
        class FakeType:
            pass
        node = TextNode("Invalid", FakeType())
        with self.assertRaises(ValueError):
            text_node_to_html_node(node)    

    def test_basic_code_block(self):
        node = TextNode("Here is `code` in text.", TextType.TEXT)
        expected = [
            TextNode("Here is ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" in text.", TextType.TEXT),
        ]
        result = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(result, expected)

    def test_multiple_code_blocks(self):
        node = TextNode("`a` and `b` are code", TextType.TEXT)
        expected = [
            TextNode("a", TextType.CODE),
            TextNode(" and ", TextType.TEXT),
            TextNode("b", TextType.CODE),
            TextNode(" are code", TextType.TEXT),
        ]
        result = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(result, expected)

    def test_bold_text(self):
        node = TextNode("This is **bold** text", TextType.TEXT)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" text", TextType.TEXT),
        ]
        result = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(result, expected)

    def test_italic_text(self):
        node = TextNode("It was _italic_ indeed", TextType.TEXT)
        expected = [
            TextNode("It was ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" indeed", TextType.TEXT),
        ]
        result = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertEqual(result, expected)

    def test_no_delimiter(self):
        node = TextNode("Nothing special here", TextType.TEXT)
        result = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(result, [node])

    def test_unmatched_delimiter(self):
        node = TextNode("Unmatched `code", TextType.TEXT)
        result = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(result, [node])

    def test_non_text_node(self):
        node = TextNode("**already bold**", TextType.BOLD)
        result = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(result, [node])

    def test_empty_text_node(self):
        node = TextNode("", TextType.TEXT)
        result = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(result, [])

    def test_link_node(self):
        node = TextNode("link", TextType.LINK, url="https://example.com")
        result = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(result, [node])

    def test_chain_split_code_and_bold(self):
        node = TextNode("this `code` is **bold**", TextType.TEXT)
        result1 = split_nodes_delimiter([node], "`", TextType.CODE)
        result2 = split_nodes_delimiter(result1, "**", TextType.BOLD)
        expected = [
            TextNode("this ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
        ]
        self.assertEqual(result2, expected)




if __name__ == "__main__":
    unittest.main()

