import unittest

from htmlnode import HTMLNode, LeafNode

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

if __name__ == "__main__":
    unittest.main()