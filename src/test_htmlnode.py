import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode

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
            LeafNode("p", None).to_html()

    def test_leaf_to_html_with_multiple_props(self):
        props = {"href": "https://example.com", "target": "_blank"}
        node = LeafNode("a", "Link", props)
        expected = '<a href="https://example.com" target="_blank">Link</a>'
        self.assertEqual(node.to_html(), expected)


class TestParentNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(),"<div><span><b>grandchild</b></span></div>",)

    def test_to_html_with_no_children(self):
        with self.assertRaises(ValueError):
            ParentNode("div", None).to_html()
    
    def test_to_html_with_multiple_children(self):
        child1 = LeafNode("span", "child1")
        child2 = LeafNode("i", "child2")
        parent_node = ParentNode("div", [child1, child2])
        self.assertEqual(parent_node.to_html(), "<div><span>child1</span><i>child2</i></div>")

    def test_to_html_with_props(self):
        child = LeafNode(None, "text")
        parent_node = ParentNode("div", [child], props={"class": "container"})
        self.assertEqual(parent_node.to_html(), '<div class="container">text</div>')

    def test_complex_nested_structure(self):
        child1 = LeafNode("b", "bold")
        child2 = ParentNode("span", [LeafNode(None, "inside span")])
        parent = ParentNode("div", [child1, child2])
    
        expected_html = "<div><b>bold</b><span>inside span</span></div>"
        self.assertEqual(parent.to_html(), expected_html)

if __name__ == "__main__":
    unittest.main()

