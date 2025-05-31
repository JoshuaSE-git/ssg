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

    def test_split_images_double(self):
        node = TextNode(
            "![image](https://i.imgur.com/zjjcJKZ.png)![image](https://i.imgur.com/zjjcJKZ.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_images([node])
        self.assertListEqual(
            [
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            ],
            new_nodes,
        )

    def test_split_links_double(self):
        node = TextNode(
            "[link](https://www.google.com)[link](https://www.google.com)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_links([node])
        self.assertListEqual(
            [
                TextNode("link", TextType.LINK, "https://www.google.com"),
                TextNode("link", TextType.LINK, "https://www.google.com"),
            ],
            new_nodes,
        )

    def test_split_all(self):
        md = ("This is **text** with an _italic_ word and a `code block` "
              + "and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)")
        new_nodes = text_to_text_nodes(md)
        self.assertListEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
            new_nodes,
        )

    def test_split_all_text_only(self):
        new_nodes = text_to_text_nodes("This is raw text only..")
        self.assertListEqual(
            [TextNode("This is raw text only..", TextType.TEXT)],
            new_nodes
        )

    def test_split_all_empty(self):
        new_nodes = text_to_text_nodes("")
        self.assertListEqual(
            [TextNode('', TextType.TEXT)],
            new_nodes
        )

    def test_split_all_error(self):
        self.assertRaises(Exception, text_to_text_nodes, "Incorrect **bold close.")

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

    def test_markdown_to_blocks_2(self):
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

    def test_markdown_to_blocks_all(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items

- another list
- with items

![solo_image](img link)

[link](link)
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
                "- another list\n- with items",
                "![solo_image](img link)",
                "[link](link)"
            ],
        )

    def test_markdown_blocks_empty(self):
        self.assertListEqual([], markdown_to_blocks(""))

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

class TestBlockFunctions(unittest.TestCase):
    def test_block_to_block_heading(self):
        self.assertEqual(block_to_block_type("# f"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("## f"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("### f"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("#### f"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("##### f"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("###### f"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("## #f#asdfsdf"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("## e #f#asdfsdf"), BlockType.HEADING)

    def test_block_to_block_code(self):
        self.assertEqual(block_to_block_type("```asfd```"), BlockType.CODE)
        self.assertEqual(block_to_block_type("```  ```"), BlockType.CODE)
        self.assertEqual(block_to_block_type("```\nasdfasd\n```"), BlockType.CODE)
        self.assertEqual(block_to_block_type("```\nasd\nasd\nasd\n```"), BlockType.CODE)

    def test_block_to_block_quote(self):
        self.assertEqual(block_to_block_type(">asdf"), BlockType.QUOTE)
        self.assertEqual(block_to_block_type(">asdf\n>asdf\n>asdf"), BlockType.QUOTE)
        self.assertEqual(block_to_block_type(">asdf\n>\n>asdf"), BlockType.QUOTE)
        self.assertEqual(block_to_block_type(">        asdf    "), BlockType.QUOTE)

    def test_block_to_block_unordered(self):
        self.assertEqual(block_to_block_type("- "), BlockType.UNORDERED_LIST)
        self.assertEqual(block_to_block_type("- hasdf"), BlockType.UNORDERED_LIST)
        self.assertEqual(block_to_block_type("-          asfd"), BlockType.UNORDERED_LIST)
        self.assertEqual(block_to_block_type("- a\n-      b\n- c"), BlockType.UNORDERED_LIST)

    def test_block_to_block_ordered(self):
        self.assertEqual(block_to_block_type("1. "), BlockType.ORDERED_LIST)
        self.assertEqual(block_to_block_type("1. \n2. \n3. "), BlockType.ORDERED_LIST)
        self.assertEqual(block_to_block_type("1. a\n2. b\n3. c"), BlockType.ORDERED_LIST)
        self.assertEqual(block_to_block_type("1. a\n2.         b\n3. c"), BlockType.ORDERED_LIST)

    def test_block_to_block_not_heading(self):
        self.assertNotEqual(block_to_block_type(" # asdfsdf"), BlockType.HEADING)
        self.assertNotEqual(block_to_block_type("asdh# asdfsdf"), BlockType.HEADING)
        self.assertNotEqual(block_to_block_type("#asdfsdf"), BlockType.HEADING)
        self.assertNotEqual(block_to_block_type("########## asdfsdf"), BlockType.HEADING)
        self.assertNotEqual(block_to_block_type("##e# asdfsdf"), BlockType.HEADING)

    def test_block_to_block_not_code(self):
        self.assertNotEqual(block_to_block_type("``asdf``"), BlockType.CODE)
        self.assertNotEqual(block_to_block_type("`asdf`"), BlockType.CODE)
        self.assertNotEqual(block_to_block_type("```asdf``"), BlockType.CODE)
        self.assertNotEqual(block_to_block_type("``asdf```"), BlockType.CODE)
        self.assertNotEqual(block_to_block_type("```asdf"), BlockType.CODE)

    def test_block_to_block_not_quote(self):
        self.assertNotEqual(block_to_block_type(">asdf\nasdf\n>asdf"), BlockType.QUOTE)

    def test_block_to_block_not_unordered(self):
        self.assertNotEqual(block_to_block_type("- sdf\nasfd\n- sdf"), BlockType.UNORDERED_LIST)
        self.assertNotEqual(block_to_block_type("-sdf\n- asfd\n- sdf"), BlockType.UNORDERED_LIST)
        self.assertNotEqual(block_to_block_type("-sdf\n-asfd\n-sdf"), BlockType.UNORDERED_LIST)
        self.assertNotEqual(block_to_block_type("--sdf"), BlockType.UNORDERED_LIST)

    def test_block_to_block_not_ordered(self):
        self.assertNotEqual(block_to_block_type("1.asdf\n2.asdf"), BlockType.ORDERED_LIST)
        self.assertNotEqual(block_to_block_type("1 asdf\n2 asdf"), BlockType.ORDERED_LIST)
        self.assertNotEqual(block_to_block_type("1. asdf\n2. asdf\n4. asdf"), BlockType.ORDERED_LIST)
        self.assertNotEqual(block_to_block_type("3. asdf\n2. asdf\n1. asdf"), BlockType.ORDERED_LIST)

    def test_block_to_block_paragraph(self):
        self.assertEqual(block_to_block_type("1.asdf\n2.asdf"), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type("1 asdf\n2 asdf"), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type("1. asdf\n2. asdf\n4. asdf"), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type("3. asdf\n2. asdf\n1. asdf"), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type("- sdf\nasfd\n- sdf"), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type("-sdf\n- asfd\n- sdf"), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type("-sdf\n-asfd\n-sdf"), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type("--sdf"), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type(">asdf\nasdf\n>asdf"), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type("``asdf``"), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type("`asdf`"), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type("```asdf``"), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type("``asdf```"), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type(" # asdfsdf"), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type("asdh# asdfsdf"), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type("#asdfsdf"), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type("########## asdfsdf"), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type("##e# asdfsdf"), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type("```asdf"), BlockType.PARAGRAPH)

    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
    )

    def test_heading(self):
        md = """
# h1

## h2

#not

####### not
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>h1</h1><h2>h2</h2><p>#not</p><p>####### not</p></div>",
    )

    def test_unordered(self):
        md = """
-     one
- **two**
- _three_
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>one</li><li><b>two</b></li><li><i>three</i></li></ul></div>",
        )
    def test_ordered(self):
        md = """
1.     one
2. **two**
3. _three_
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ol><li>one</li><li><b>two</b></li><li><i>three</i></li></ol></div>",
        )

    def test_quote(self):
        md = """
>q1
>      q2
>q3
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote><p>q1</p><p>q2</p><p>q3</p></blockquote></div>",
        )

    def test_quote_empty(self):
        md = """
>q1
> 
>q3
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote><p>q1</p><p></p><p>q3</p></blockquote></div>",
        )

    def test_all(self):
        md = """
# h1

This is a
**paragraph**
_block_ `code`

- u1
- u2




1. o1
2. o2

###### h6

![image](url)

A para with [link](url)




** edge **
**edge **
** edge**
_ edge _
_edge _
_ edge_
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.maxDiff = None
        self.assertEqual(
            html,
            "<div><h1>h1</h1><p>This is a <b>paragraph</b> <i>block</i> " +
            "<code>code</code></p><ul><li>u1</li><li>u2</li></ul><ol><li>o1" +
            "</li><li>o2</li></ol><h6>h6</h6><p><img src=\"url\" alt=\"image\" /></p>" +
            "<p>A para with <a href=\"url\">link</a></p>" +
            "<p>** edge ** **edge ** ** edge** _ edge _ _edge _ _ edge_</p></div>",
        )


if __name__ == "__main__":
    unittest.main()
