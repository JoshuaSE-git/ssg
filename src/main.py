from textnode import TextType, TextNode

def main():
    text_node = TextNode("Sample text", TextType.NORMAL, "https://www.boot.dev")
    print(text_node)

main()