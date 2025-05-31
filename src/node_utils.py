import re

from textnode import *
from htmlnode import *

def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType) -> list[TextNode]:
    new_nodes = []
    for node in old_nodes:
        if node.text_type == TextType.TEXT:
            split_nodes = []
            split_text = node.text.split(delimiter)
            if len(split_text) % 2 == 0:
                raise Exception(f"Missing delimiter in: {node}")
            for i in range(len(split_text)):
                if i % 2 == 1:
                    if split_text[i].startswith(" ") or split_text[i].endswith(" "):
                        split_nodes.append(TextNode(delimiter + split_text[i] + delimiter, TextType.TEXT))
                    else:
                        split_nodes.append(TextNode(split_text[i], text_type))
                elif len(split_text[i]) > 0:
                    split_nodes.append(TextNode(split_text[i], TextType.TEXT))
            new_nodes.extend(split_nodes)
        else:
            new_nodes.append(node)

    return new_nodes

def extract_markdown_images(text: str) -> list[tuple[str, str]]:
    return re.findall(r"!\[([^\[\]]*)]\(([^()]*)\)", text)

def extract_markdown_links(text: str) -> list[tuple[str, str]]:
    return re.findall(r"(?<!!)\[([^\[\]]*)]\(([^()]*)\)", text)

def split_nodes_images(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []
    for node in old_nodes:
        if node.text_type == TextType.TEXT:
            node_string = node.text
            img_tuples_list = extract_markdown_images(node_string)
            if len(img_tuples_list) == 0:
                new_nodes.append(node)
            else:
                for img in img_tuples_list:
                    split_string = node_string.split(f"![{img[0]}]({img[1]})", 1)
                    if len(split_string[0]) > 0:
                        new_nodes.append(TextNode(split_string[0], TextType.TEXT))
                    new_nodes.append(TextNode(img[0], TextType.IMAGE, img[1]))
                    node_string = split_string[1]

                if len(node_string) > 0:
                    new_nodes.append(TextNode(node_string, TextType.TEXT))
        else:
            new_nodes.append(node)

    return new_nodes

def split_nodes_links(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []
    for node in old_nodes:
        if node.text_type == TextType.TEXT:
            node_string = node.text
            link_tuples_list = extract_markdown_links(node_string)
            if len(link_tuples_list) == 0:
                new_nodes.append(node)
            else:
                for link in link_tuples_list:
                    split_string = node_string.split(f"[{link[0]}]({link[1]})", 1)
                    if len(split_string[0]) > 0:
                        new_nodes.append(TextNode(split_string[0], TextType.TEXT))
                    new_nodes.append(TextNode(link[0], TextType.LINK, link[1]))
                    node_string = split_string[1]

                if len(node_string) > 0:
                    new_nodes.append(TextNode(node_string, TextType.TEXT))
        else:
            new_nodes.append(node)

    return new_nodes

def text_to_text_nodes(text: str) -> list[TextNode]:
    if len(text) < 1:
        return [TextNode('', TextType.TEXT)]
    split_bold = split_nodes_delimiter([TextNode(text, TextType.TEXT)], "**", TextType.BOLD)
    split_italic = split_nodes_delimiter(split_bold, "_", TextType.ITALIC)
    split_code = split_nodes_delimiter(split_italic, "`", TextType.CODE)
    split_images = split_nodes_images(split_code)
    split_links = split_nodes_links(split_images)

    return split_links

def markdown_to_blocks(text: str) -> list[str]:
    blocks = text.split("\n\n")
    filtered_blocks = filter(lambda x: len(x) > 0, blocks)
    stripped_blocks = map(lambda x: x.strip(), filtered_blocks)
    return list(stripped_blocks)

class BlockType(Enum):
    HEADING = "heading"
    PARAGRAPH = "paragraph"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def block_to_block_type(block: str) -> BlockType:
    if block.startswith("```") and block.endswith("```"):
        return BlockType.CODE
    if is_heading(block):
        return BlockType.HEADING
    lines = block.split("\n")
    if all_begins_with(lambda x: x.startswith("- "), lines):
        return BlockType.UNORDERED_LIST
    if all_begins_with(lambda x: x.startswith(">"), lines):
        return BlockType.QUOTE
    order_tracker = create_order_tracker(0)
    if all_begins_with(lambda x: x[0].isdigit() and order_tracker(x) and x.startswith(". ", 1), lines):
        return BlockType.ORDERED_LIST

    return BlockType.PARAGRAPH

def all_begins_with(func, lines: list[str]) -> bool:
    for line in lines:
        if not func(line):
            return False
    return True

def create_order_tracker(start: int):
    curr_num = start
    def inner_func(line):
        nonlocal curr_num
        curr_num += 1
        return int(line[0]) == curr_num
    return inner_func

def is_heading(block: str) -> bool:
    parts = block.partition(" ")
    if 0 < len(parts[0]) < 7 and len(parts[2]) > 0:
        for c in parts[0]:
            if c != "#":
                return False
        return True
    return False

def markdown_to_html_node(md: str) -> HTMLNode:
    children = list(map(block_to_html_node, markdown_to_blocks(md)))
    return ParentNode("div", children)

def block_to_html_node(block: str) -> ParentNode:
    tag_map = {
        BlockType.HEADING: "",
        BlockType.QUOTE: "blockquote",
        BlockType.CODE: "pre",
        BlockType.ORDERED_LIST: "ol",
        BlockType.UNORDERED_LIST: "ul",
        BlockType.PARAGRAPH: "p"
    }
    block_type = block_to_block_type(block)
    if block_type == BlockType.HEADING:
        tag_map[BlockType.HEADING] = f"h{len(block.split(" ", maxsplit=1)[0])}"

    return ParentNode(tag_map[block_type], text_to_children(block))

def text_to_children(block: str) -> list[HTMLNode]:
    match block_to_block_type(block):
        case BlockType.PARAGRAPH:
            return text_to_leaf_nodes(block.replace("\n", " "))
        case BlockType.CODE:
            return [ParentNode("code", [LeafNode(None, block.split("```")[1].lstrip("\n"))])]
        case BlockType.QUOTE:
            return get_multi_line_children(block, "p", ">")
        case BlockType.ORDERED_LIST:
            return get_multi_line_children(block, "li", " ")
        case BlockType.UNORDERED_LIST:
            return get_multi_line_children(block, "li", " ")
        case BlockType.HEADING:
            return text_to_leaf_nodes(block.split(" ", maxsplit=1)[1])
        case _:
            raise Exception("Invalid BlockType")

def get_multi_line_children(block: str, tag: str | None, delim: str) -> list[HTMLNode]:
    lines = block.split("\n")
    children = []
    for line in lines:
            children.append(ParentNode(tag, text_to_leaf_nodes(line.split(delim, maxsplit=1)[1].strip(" "))))
    return children

def text_to_leaf_nodes(text: str) -> list[LeafNode]:
    text_nodes = text_to_text_nodes(text)
    return list(map(text_node_to_html_node, text_nodes))



