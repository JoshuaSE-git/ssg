from functools import reduce

class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self):
        if self.props is None:
            return ""

        prop_str = reduce(lambda prev_str, tup: prev_str + f' {tup[0]}="{tup[1]}"', self.props.items(), "")

        return prop_str

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, props=props)

    def to_html(self):
        if self.value is None:
            raise ValueError("LeafNode must contain value.")
        if self.tag is None:
            return self.value
        if self.tag == "img":
            return f"<{self.tag}{self.props_to_html()} />"

        html_str = f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

        return html_str

    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})"

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag=tag, children=children, props=props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("ParentNode must contain tag.")
        if self.children is None or len(self.children) < 1:
            raise ValueError("ParentNode must contain children nodes.")

        children_str = reduce(lambda prev_str, curr: prev_str + curr.to_html(), self.children, "")
        html_str = f"<{self.tag}{self.props_to_html()}>{children_str}</{self.tag}>"

        return html_str

    def __repr__(self):
        return f"ParentNode({self.tag}, {self.children}, {self.props})"

