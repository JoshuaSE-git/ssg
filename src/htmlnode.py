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

        prop_str = reduce(
            lambda prev_str, tup: prev_str + f' {tup[0]}="{tup[1]}"',
            self.props.items(),
            ""
        )
        return prop_str

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"
