from textnode import TextType, TextNode
from htmlnode import HTMLNode, LeafNode, ParentNode

def main():
    text_node = TextNode("Sample text", TextType.NORMAL, "https://www.boot.dev")
    print(text_node)

if __name__ == "__main__":
    main()