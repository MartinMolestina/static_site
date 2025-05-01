import unittest
from markdown_parser import extract_markdown_images, extract_markdown_links, split_nodes_link, split_nodes_image
from textnode import TextNode, TextType


class TestMarkdownParser(unittest.TestCase):
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_multiple_images(self):
        matches = extract_markdown_images(
            "Images: ![one](https://img.com/1.png) and ![two](https://img.com/2.jpg)"
        )
        self.assertListEqual([
            ("one", "https://img.com/1.png"),
            ("two", "https://img.com/2.jpg")
        ], matches)

    def test_extract_image_with_spaces(self):
        matches = extract_markdown_images(
            "Image: ![ spaced alt ] ( https://img.com/spaced.png )"
        )
        self.assertListEqual([
            ("spaced alt", "https://img.com/spaced.png")
        ], matches)

    def test_extract_image_with_empty_alt(self):
        matches = extract_markdown_images("Check this ![](https://img.com/blank.png)")
        self.assertListEqual([
            ("", "https://img.com/blank.png")
        ], matches)

    def test_extract_image_no_match(self):
        matches = extract_markdown_images("This has no images.")
        self.assertListEqual([], matches)


    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "Visit [Boot.dev](https://www.boot.dev)"
        )
        self.assertListEqual([
            ("Boot.dev", "https://www.boot.dev")
        ], matches)

    def test_extract_multiple_links(self):
        matches = extract_markdown_links(
            "[Google](https://google.com) and [YouTube](https://youtube.com)"
        )
        self.assertListEqual([
            ("Google", "https://google.com"),
            ("YouTube", "https://youtube.com")
        ], matches)

    def test_extract_link_with_spaces(self):
        matches = extract_markdown_links(
            "Click [ spaced link ] ( https://example.com )"
        )
        self.assertListEqual([
            ("spaced link", "https://example.com")
        ], matches)

    def test_extract_link_empty_anchor(self):
        matches = extract_markdown_links("Empty: [](https://blank.com)")
        self.assertListEqual([
            ("", "https://blank.com")
        ], matches)

    def test_extract_link_ignores_images(self):
        matches = extract_markdown_links("This is an image: ![pic](https://img.com)")
        self.assertListEqual([], matches)

    def test_split_links(self):
        node = TextNode(
            "Here's a [link](https://example.com) and another [second](https://2.com)",
            TextType.TEXT
        )
        result = split_nodes_link([node])
        self.assertListEqual([
            TextNode("Here's a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://example.com"),
            TextNode(" and another ", TextType.TEXT),
            TextNode("second", TextType.LINK, "https://2.com"),
        ], result)

    def test_split_link_with_empty_anchor(self):
        node = TextNode("Here: [](https://blank.com)", TextType.TEXT)
        result = split_nodes_link([node])
        self.assertListEqual([
            TextNode("Here: ", TextType.TEXT),
            TextNode("", TextType.LINK, "https://blank.com")
        ], result)

    def test_split_link_only(self):
        node = TextNode("[x](y.com)", TextType.TEXT)
        result = split_nodes_link([node])
        self.assertListEqual([TextNode("x", TextType.LINK, "y.com")], result)

    def test_split_link_with_text_before_after(self):
        node = TextNode("a [link](z.com) b", TextType.TEXT)
        result = split_nodes_link([node])
        self.assertListEqual([
            TextNode("a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "z.com"),
            TextNode(" b", TextType.TEXT)
        ], result)

    def test_split_link_ignores_images(self):
        node = TextNode("![not a link](img.com)", TextType.TEXT)
        result = split_nodes_link([node])
        self.assertListEqual([node], result)

    def test_split_link_ignores_non_text_nodes(self):
        node = TextNode("anchor", TextType.LINK, "https://boot.dev")
        result = split_nodes_link([node])
        self.assertListEqual([node], result)
