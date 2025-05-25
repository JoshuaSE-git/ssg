import unittest

from node_utils import *
from textnode import *
from htmlnode import *

class TestSplitNodes(unittest.TestCase):
    def test_split_bold(self):
        node = TextNode("This is **bold** node.", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        correct = [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" node.", TextType.TEXT)
        ]
        self.assertEqual(new_nodes, correct)

    def test_split_italic(self):
        node = TextNode("This is an _italic_ node.", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        correct = [
            TextNode("This is an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" node.", TextType.TEXT)
        ]
        self.assertEqual(new_nodes, correct)

    def test_split_code(self):
        node = TextNode("This is a `code` node.", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        correct = [
            TextNode("This is a ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" node.", TextType.TEXT)
        ]
        self.assertEqual(new_nodes, correct)

    def test_split_missing_delim(self):
        node = TextNode("This is a `code node.", TextType.TEXT)
        self.assertRaises(Exception, split_nodes_delimiter, node)

    def test_split_multiple_type(self):
        node = TextNode("This is _one_ and _two_", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        correct = [
            TextNode("This is ", TextType.TEXT),
            TextNode("one", TextType.ITALIC),
            TextNode(" and ", TextType.TEXT),
            TextNode("two", TextType.ITALIC)
        ]
        self.assertEqual(new_nodes, correct)

    def test_split_solo_type(self):
        node = TextNode("**one**", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        correct = [
            TextNode("one", TextType.BOLD)
        ]
        self.assertEqual(new_nodes, correct)

    def test_split_no_space(self):
        node = TextNode("thisis**one**end.", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        correct = [
            TextNode("thisis", TextType.TEXT),
            TextNode("one", TextType.BOLD),
            TextNode("end.", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, correct)

    def test_split_multi_node(self):
        old_nodes = [
            TextNode("1", TextType.TEXT),
            TextNode("I need **split** func.", TextType.TEXT),
            TextNode("interleaved", TextType.ITALIC),
            TextNode("text", TextType.TEXT),
            TextNode("I also need **split** func.", TextType.TEXT),
            TextNode("Last node", TextType.TEXT)
        ]
        new_nodes = split_nodes_delimiter(old_nodes, "**", TextType.BOLD)
        correct= [
            TextNode("1", TextType.TEXT),
            TextNode("I need ", TextType.TEXT),
            TextNode("split", TextType.BOLD),
            TextNode(" func.", TextType.TEXT),
            TextNode("interleaved", TextType.ITALIC),
            TextNode("text", TextType.TEXT),
            TextNode("I also need ", TextType.TEXT),
            TextNode("split", TextType.BOLD),
            TextNode(" func.", TextType.TEXT),
            TextNode("Last node", TextType.TEXT)
        ]
        self.assertEqual(new_nodes, correct)

    def test_split_no_match(self):
        node = TextNode("thisis**one**end.", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        correct = [
            TextNode("thisis**one**end.", TextType.TEXT)
        ]
        self.assertEqual(new_nodes, correct)

class TestExtraction(unittest.TestCase):
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a [link](https://www.google.com)"
        )
        self.assertListEqual([("link", "https://www.google.com")], matches)

    def test_extract_markdown_images_combined(self):
        matches = extract_markdown_images(
            "This is text with a [link](https://www.google.com) and ![an image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("an image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_links_combined(self):
        matches = extract_markdown_links(
            "This is text with a [link](https://www.google.com) and ![an image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("link", "https://www.google.com")], matches)

    def test_extract_markdown_images_no_matches(self):
        matches = extract_markdown_images(
            "no matches"
        )
        self.assertListEqual([], matches)

    def test_extract_markdown_links_no_matches(self):
        matches = extract_markdown_links(
            "no matches"
        )
        self.assertListEqual([], matches)

    def test_extract_markdown_links_multi(self):
        matches = extract_markdown_links(
            "This is text with a [link](https://www.google.com) and [link2](https://www.youtube.com)"
        )
        self.assertListEqual([("link", "https://www.google.com"), ("link2", "https://www.youtube.com")], matches)

    def test_extract_markdown_images_multi(self):
        matches = extract_markdown_images(
            "This is text with a ![image](https://i.imgur.com/zjjcJKZ.png) and ![image2](https://i.imgur.com/zzzcaxZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png"), ("image2", "https://i.imgur.com/zzzcaxZ.png")], matches)




if __name__ == "__main__":
    unittest.main()
