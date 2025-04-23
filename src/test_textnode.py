import unittest
from textnode import TextNode, TextType


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


if __name__ == "__main__":
    unittest.main()

