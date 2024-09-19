import unittest

from textnode import *


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", "bold")
        node2 = TextNode("This is a text node", "bold")
        self.assertEqual(node, node2)

    def test_not_eq_text(self):
        node = TextNode("This is a text node", "bold")
        node2 = TextNode("This is a different text node", "bold")
        self.assertNotEqual(node, node2)

    def test_not_eq_text_type(self):
        node = TextNode("This is a text node", "bold")
        node2 = TextNode("This is a text node", "italic")
        self.assertNotEqual(node, node2)

    def test_not_eq_url(self):
        node = TextNode("This is a text node", "bold")
        node2 = TextNode("This is a text node", "bold", "some url")
        self.assertNotEqual(node, node2)

    def test_repr(self):
        node = TextNode("This is a text node", "text", "https://www.boot.dev")
        self.assertEqual("TextNode(This is a text node, text, https://www.boot.dev)", repr(node))


class TestTextNodeToHTMLNode(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node", text_type_text)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_image(self):
        node = TextNode("This is an image", text_type_image, "https://www.boot.dev")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(
            html_node.props,
            {"src": "https://www.boot.dev", "alt": "This is an image"},
        )

    def test_bold(self):
        node = TextNode("This is bold", text_type_bold)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is bold")


class TestSplitNodesDelimiter(unittest.TestCase):
    def test_code(self):
        node = TextNode("This is text with a `code block` word", text_type_text)
        new_nodes = split_nodes_delimiter([node], "`", text_type_code)
        self.assertEqual(new_nodes, [
                TextNode("This is text with a ", text_type_text),
                TextNode("code block", text_type_code),
                TextNode(" word", text_type_text),
            ]
        )

    def test_italic(self):
        node = TextNode("This is text with an *italic block* word", text_type_text)
        new_nodes = split_nodes_delimiter([node], "*", text_type_italic)
        self.assertEqual(new_nodes, [
                TextNode("This is text with an ", text_type_text),
                TextNode("italic block", text_type_italic),
                TextNode(" word", text_type_text),
            ]
        )

    def test_bold(self):
        node = TextNode("This is text with a **bold block** word", text_type_text)
        new_nodes = split_nodes_delimiter([node], "**", text_type_bold)
        self.assertEqual(new_nodes, [
                TextNode("This is text with a ", text_type_text),
                TextNode("bold block", text_type_bold),
                TextNode(" word", text_type_text),
            ]
        )

    def test_list(self):
        node = TextNode("This is text with a `code block` word", text_type_text)
        node2 = TextNode("This is also text with a `code block` word", text_type_text)
        new_nodes = split_nodes_delimiter([node, node2], "`", text_type_code)
        self.assertEqual(new_nodes, [
                TextNode("This is text with a ", text_type_text),
                TextNode("code block", text_type_code),
                TextNode(" word", text_type_text),
                TextNode("This is also text with a ", text_type_text),
                TextNode("code block", text_type_code),
                TextNode(" word", text_type_text),
            ]
        )

    def test_multiple_same(self):
        node = TextNode("This is text with a **bold block** word and another **bold block** word", text_type_text)
        new_nodes = split_nodes_delimiter([node], "**", text_type_bold)
        self.assertEqual(new_nodes, [
                TextNode("This is text with a ", text_type_text),
                TextNode("bold block", text_type_bold),
                TextNode(" word and another ", text_type_text),
                TextNode("bold block", text_type_bold),
                TextNode(" word", text_type_text),
            ]
        )

    def test_bold_and_italic(self):
        node = TextNode("This is text with a **bold block** word and an *italic block* aswell", text_type_text)
        new_nodes = split_nodes_delimiter([node], "**", text_type_bold)
        self.assertEqual(new_nodes, [
                TextNode("This is text with a ", text_type_text),
                TextNode("bold block", text_type_bold),
                TextNode(" word and an *italic block* aswell", text_type_text),
            ]
        )

    def test_italic_and_bold(self):
        node = TextNode("This is text with a **bold block** word and an *italic block* aswell", text_type_text)
        new_nodes = split_nodes_delimiter([node], "*", text_type_italic)
        self.assertEqual(new_nodes, [
                TextNode("This is text with a ", text_type_text),
                TextNode("bold block", text_type_text),
                TextNode(" word and an ", text_type_text),
                TextNode("italic block", text_type_italic),
                TextNode(" aswell", text_type_text),
            ]
        )

    def test_extract_markdown_images(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        self.assertEqual(extract_markdown_images(text), [("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")])


    def test_extract_markdown_links(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        self.assertEqual(extract_markdown_links(text), [("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")])

    def test_split_nodes_images(self):
        node = TextNode(
            "This is text with a link ![to boot dev](https://www.boot.dev) and ![to youtube](https://www.youtube.com/@bootdotdev)",
            text_type_text,
        )
        new_nodes = split_nodes_image([node])
        self.assertEqual(new_nodes,
                            [
                                TextNode("This is text with a link ", text_type_text),
                                TextNode("to boot dev", text_type_image, "https://www.boot.dev"),
                                TextNode(" and ", text_type_text),
                                TextNode(
                                    "to youtube", text_type_image, "https://www.youtube.com/@bootdotdev"
                                ),
                            ]
                         
                        )
        
    def test_split_nodes_images_end_text(self):
        node = TextNode(
            "This is text with a link ![to boot dev](https://www.boot.dev) and ![to youtube](https://www.youtube.com/@bootdotdev) awesome!",
            text_type_text,
        )
        new_nodes = split_nodes_image([node])
        self.assertEqual(new_nodes,
                            [
                                TextNode("This is text with a link ", text_type_text),
                                TextNode("to boot dev", text_type_image, "https://www.boot.dev"),
                                TextNode(" and ", text_type_text),
                                TextNode(
                                    "to youtube", text_type_image, "https://www.youtube.com/@bootdotdev"
                                ),
                                TextNode(" awesome!", text_type_text)
                            ]
                         
                        )

    def test_split_multiple_nodes_images(self):
        node2 = TextNode(
            "This is text with a link ![to boot dev](https://www.boot.dev) and ![to youtube](https://www.youtube.com/@bootdotdev)",
            text_type_text,
        )
        node = TextNode(
            "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)",
            text_type_text,
        )
        new_nodes = split_nodes_image([node, node2])
        self.assertEqual(new_nodes,
                            [
                                TextNode("This is text with a ", text_type_text),
                                TextNode("rick roll", text_type_image, "https://i.imgur.com/aKaOqIh.gif"),
                                TextNode(" and ", text_type_text),
                                TextNode(
                                    "obi wan", text_type_image, "https://i.imgur.com/fJRm4Vk.jpeg"
                                ),                                
                                TextNode("This is text with a link ", text_type_text),
                                TextNode("to boot dev", text_type_image, "https://www.boot.dev"),
                                TextNode(" and ", text_type_text),
                                TextNode(
                                    "to youtube", text_type_image, "https://www.youtube.com/@bootdotdev"
                                ),
                            ]
                         
                        )

    def test_split_nodes_links(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            text_type_text,
        )
        new_nodes = split_nodes_link([node])
        self.assertEqual(new_nodes,
                            [
                                TextNode("This is text with a link ", text_type_text),
                                TextNode("to boot dev", text_type_link, "https://www.boot.dev"),
                                TextNode(" and ", text_type_text),
                                TextNode(
                                    "to youtube", text_type_link, "https://www.youtube.com/@bootdotdev"
                                ),
                            ]
                         
                        )

    def test_split_nodes_links_end_text(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev) awesome!",
            text_type_text,
        )
        new_nodes = split_nodes_link([node])
        self.assertEqual(new_nodes,
                            [
                                TextNode("This is text with a link ", text_type_text),
                                TextNode("to boot dev", text_type_link, "https://www.boot.dev"),
                                TextNode(" and ", text_type_text),
                                TextNode(
                                    "to youtube", text_type_link, "https://www.youtube.com/@bootdotdev"
                                ),
                                TextNode(" awesome!", text_type_text)
                            ]
                         
                        )

    def test_split_multiple_nodes_single_link(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev)",
            text_type_text,
        )
        node2 = TextNode(
            "This is text with a link [to youtube](https://www.youtube.com/@bootdotdev)",
            text_type_text,
        )
        new_nodes = split_nodes_link([node, node2])
        self.assertEqual(new_nodes,
                            [
                                TextNode("This is text with a link ", text_type_text),
                                TextNode("to boot dev", text_type_link, "https://www.boot.dev"),
                                TextNode("This is text with a link ", text_type_text),
                                TextNode(
                                    "to youtube", text_type_link, "https://www.youtube.com/@bootdotdev"
                                ),
                            ]
                         
                        )

    def test_text_to_textnodes(self):
        text = "This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        node_list = text_to_textnodes(text)
        self.assertEqual(node_list,
                         [
                            TextNode("This is ", text_type_text),
                            TextNode("text", text_type_bold),
                            TextNode(" with an ", text_type_text),
                            TextNode("italic", text_type_italic),
                            TextNode(" word and a ", text_type_text),
                            TextNode("code block", text_type_code),
                            TextNode(" and an ", text_type_text),
                            TextNode("obi wan image", text_type_image, "https://i.imgur.com/fJRm4Vk.jpeg"),
                            TextNode(" and a ", text_type_text),
                            TextNode("link", text_type_link, "https://boot.dev"),
                        ]
        )

if __name__ == "__main__":
    unittest.main()