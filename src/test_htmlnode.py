import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode

class TestHTMLNode(unittest.TestCase):
    def test_props_to_html_none(self):
        node = HTMLNode()
        self.assertEqual(node.props_to_html(), "")

    def test_props_to_html(self):
        props = {
            "href": "https://www.google.com",
            "target": "_blank"
        }
        prop_str = f' href="https://www.google.com" target="_blank"'
        node = HTMLNode(props=props)
        self.assertEqual(node.props_to_html(), prop_str)

    def test_props_to_html_empty(self):
        node = HTMLNode(props={})
        self.assertEqual(node.props_to_html(), "")

    def test_repr_default(self):
        node = HTMLNode()
        node_str = "HTMLNode(None, None, None, None)"
        self.assertEqual(node.__repr__(), node_str)

    def test_repr(self):
        node = HTMLNode("p", "text")
        node_str = 'HTMLNode(p, text, None, None)'
        self.assertEqual(node.__repr__(), node_str)

class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_no_tag(self):
        node = LeafNode(None, "value text.")
        html_str = "value text."
        self.assertEqual(node.to_html(), html_str)

    def test_leaf_to_html_no_val(self):
        node = LeafNode(None, None)
        self.assertRaises(ValueError, node.to_html)

    def test_leaf_to_html_no_props(self):
        node = LeafNode("p", "value text.")
        html_str = f'<p>value text.</p>'
        self.assertEqual(node.to_html(), html_str)

    def test_leaf_to_html_w_props(self):
        props = {
            "href": "https://www.google.com",
            "hreflang": "en"
        }
        node = LeafNode("a", "value text.", props)
        html_str = f'<a href="https://www.google.com" hreflang="en">value text.</a>'
        self.assertEqual(node.to_html(), html_str)

class TestParentNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_with_grandchildren_2(self):
        children = [
            LeafNode(None, "raw text"),
            ParentNode("p",[LeafNode(None, "raw gc text")],{"style": "text-align:right"}),
            ParentNode("p", [LeafNode("b", "raw gc text2")]),
            LeafNode("p", "leaf text", props={"id": "hi"})
        ]
        node = ParentNode("body", children=children)
        html_str = ('<body>raw text<p style="text-align:right">raw gc text</p>'
                    + '<p><b>raw gc text2</b></p><p id="hi">leaf text</p></body>')
        self.assertEqual(node.to_html(), html_str)

    def test_to_html_with_grandchildren_3(self):
        ggc = LeafNode("b", "bold text", {"id": "test"})
        gc = ParentNode("span", [ggc])
        c = ParentNode("p", [gc])
        parent = ParentNode("body", [c], {"id": "body"})
        html_str = '<body id="body"><p><span><b id="test">bold text</b></span></p></body>'
        self.assertEqual(parent.to_html(), html_str)

    def test_to_html_no_children(self):
        node = ParentNode("body", None)
        self.assertRaises(ValueError, node.to_html)
        node2 = ParentNode("body", [])
        self.assertRaises(ValueError, node.to_html)

    def test_to_html_no_tag(self):
        node = ParentNode(None, [LeafNode(None, "text")])
        self.assertRaises(ValueError, node.to_html)

if __name__ == "__main__":
    unittest.main()