from textnode import TextNode

def main():
    text_node = TextNode("test", "123", "test")
    text_node2 = TextNode("test", "123", "test")
    print(repr(text_node))
    print(repr(text_node2))
    print(text_node == text_node2)

main()