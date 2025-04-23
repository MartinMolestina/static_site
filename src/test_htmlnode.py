import unittest

from htmlnode import HTMLNode, LeafNode

class testHTMLNode(unittest.TestCase):
    def test_props_to_html_single(self):
        node = HTMLNode(tag="a", value="Click", props={"href": "https://example.com"})
        self.assertEqual(node.props_to_html(), ' href="https://example.com"')

    def test_props_to_html_multiple(self):
        props = {"href": "https://example.com", "class": "btn"}
        node = HTMLNode(tag="a", value="Click", props=props)
        html_props = node.props_to_html()
        # Check that both props exist in the result
        self.assertIn('href="https://example.com"', html_props)
        self.assertIn('class="btn"', html_props)

    def test_props_to_html_empty(self):
        node = HTMLNode(tag="div")
        self.assertEqual(node.props_to_html(), "")


class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_a_with_props(self):
        node = LeafNode("a", "Click me!", {"href": "https://example.com"})
        self.assertEqual(node.to_html(), '<a href="https://example.com">Click me!</a>')

    def test_leaf_to_html_strong(self):
        node = LeafNode("strong", "Bold text")
        self.assertEqual(node.to_html(), "<strong>Bold text</strong>")

    def test_leaf_to_html_raw_text(self):
        node = LeafNode(None, "Just plain text.")
        self.assertEqual(node.to_html(), "Just plain text.")

    def test_leaf_to_html_raises_if_value_none(self):
        with self.assertRaises(ValueError):
            LeafNode("p", None)

    def test_leaf_to_html_with_multiple_props(self):
        props = {"href": "https://example.com", "target": "_blank"}
        node = LeafNode("a", "Link", props)
        expected = '<a href="https://example.com" target="_blank">Link</a>'
        self.assertEqual(node.to_html(), expected)


if __name__ == "__main__":
    unittest.main()

