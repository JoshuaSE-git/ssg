import unittest

from node_utils import *
from textnode import *

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

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png).",
            TextType.TEXT,
        )
        new_nodes = split_nodes_images([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
                TextNode(".", TextType.TEXT)
            ],
            new_nodes,
    )

    def test_split_links(self):
        node = TextNode(
            "This is text with an [link](https://www.google.com) and another [link2](https://www.youtube.com).",
            TextType.TEXT,
        )
        new_nodes = split_nodes_links([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://www.google.com"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "link2", TextType.LINK, "https://www.youtube.com"
                ),
                TextNode(".", TextType.TEXT)
            ],
            new_nodes,
        )

    def test_split_links_combined(self):
        node = TextNode(
            "This is text with an [link](https://www.google.com) and another ![image](https://i.imgur.com/zjjcJKZ.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_links([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://www.google.com"),
                TextNode(" and another ![image](https://i.imgur.com/zjjcJKZ.png)", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_images_combined(self):
        node = TextNode(
            "This is text with an [link](https://www.google.com) and another ![image](https://i.imgur.com/zjjcJKZ.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_images([node])
        self.assertListEqual(
            [
                TextNode("This is text with an [link](https://www.google.com) and another ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            ],
            new_nodes,
        )

    def test_split_links_no_match(self):
        node = TextNode(
            "This is text with a ![image](https://i.imgur.com/zjjcJKZ.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_links([node])
        self.assertListEqual(
            [node],
            new_nodes,
        )

    def test_split_images_no_match(self):
        node = TextNode(
            "This is text with an [link](https://www.google.com)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_images([node])
        self.assertListEqual(
            [node],
            new_nodes,
        )

    def test_split_links_only(self):
        node = TextNode(
            "[link](https://www.google.com)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_links([node])
        self.assertListEqual(
            [TextNode("link", TextType.LINK, "https://www.google.com")],
            new_nodes,
        )

    def test_split_images_only(self):
        node = TextNode(
            "![image](https://i.imgur.com/zjjcJKZ.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_images([node])
        self.assertListEqual(
            [TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png")],
            new_nodes,
        )

    def test_split_images_multi(self):
        node = TextNode(
            "![image](https://i.imgur.com/zjjcJKZ.png)",
            TextType.TEXT,
        )
        node2 = TextNode(
            "This is text with a ![image](https://i.imgur.com/zjjcJKZ.png).",
            TextType.TEXT,
        )
        new_nodes = split_nodes_images(
            [
                TextNode("text", TextType.TEXT),
                node2,
                TextNode("bold", TextType.BOLD),
                node
            ]
        )
        self.assertListEqual(
            [
                TextNode("text", TextType.TEXT),
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(".", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png")
            ],
            new_nodes,
        )

    def test_split_links_multi(self):
        node = TextNode(
            "[link](https://www.google.com)",
            TextType.TEXT,
        )
        node2 = TextNode(
            "This is text with a [link](https://www.youtube.com).",
            TextType.TEXT,
        )
        new_nodes = split_nodes_links(
            [
                TextNode("text", TextType.TEXT),
                node2,
                TextNode("bold", TextType.BOLD),
                node
            ]
        )
        self.assertListEqual(
            [
                TextNode("text", TextType.TEXT),
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://www.youtube.com"),
                TextNode(".", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode("link", TextType.LINK, "https://www.google.com")
            ],
            new_nodes,
        )

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
