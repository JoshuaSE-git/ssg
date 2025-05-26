import re

from textnode import TextNode, TextType

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
    split_bold = split_nodes_delimiter([TextNode(text, TextType.TEXT)], "**", TextType.BOLD)
    split_italic = split_nodes_delimiter(split_bold, "_", TextType.ITALIC)
    split_code = split_nodes_delimiter(split_italic, "`", TextType.CODE)
    split_images = split_nodes_images(split_code)
    split_links = split_nodes_links(split_images)

    return split_links


def markdown_to_blocks(text: str) -> list[str]:
    blocks = text.split("\n\n")
    filtered_blocks = filter(lambda x: len(x) > 0, blocks)
    stripped_blocks = map(str.strip, filtered_blocks)
    return list(stripped_blocks)