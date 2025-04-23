import unittest

from htmlnode import HTMLNode

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

if __name__ == "__main__":
    unittest.main()
