from htmlnode import LeafNode
import re

text_type_text = "text"
text_type_bold = "bold"
text_type_italic = "italic"
text_type_code = "code"
text_type_link = "link"
text_type_image = "image"


class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        if (
        self.text == other.text
        and self.text_type == other.text_type
        and self.url == other.url
        ):
            return True
        else:
            return False
    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type}, {self.url})"
    
def text_node_to_html_node(text_node):
    if text_node.text_type == text_type_text:
        return LeafNode(None, text_node.text)
    if text_node.text_type == text_type_bold:
        return LeafNode("b", text_node.text)
    if text_node.text_type == text_type_italic:
        return LeafNode("i", text_node.text)
    if text_node.text_type == text_type_code:
        return LeafNode("code", text_node.text)
    if text_node.text_type == text_type_link:
        return LeafNode("a", text_node.text, {"href": text_node.url})
    if text_node.text_type == text_type_image:
        return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
    raise ValueError(f"Invalid text type: {text_node.text_type}")

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    return_list = []
    for node in old_nodes:
        if node.text_type != text_type_text:
            return_list.append(node)
        else:
            split = node.text.split(delimiter)
            if len(split) % 2 == 0:
                raise Exception("Invalid Markdown, formatted section not closed")
            count = 0
            new_list = []
            for string in split:
                if string == "":
                    count += 1
                    continue
                if count % 2 == 0:
                    new_list.append(TextNode(string, text_type_text))
                    count += 1
                else:
                    new_list.append(TextNode(string, text_type))
                    count += 1
            return_list.extend(new_list)
    return return_list

def extract_markdown_images(text):
    matches = re.findall(r"!\[(.*?)\]\((.*?)\)", text)
    return matches

def extract_markdown_links(text):
    matches = re.findall(r"(?<!!)\[(.*?)\]\((.*?)\)", text)
    return matches

def split_nodes_image(old_nodes):
    return_list = []
    for node in old_nodes:
        extracted = extract_markdown_images(node.text)
        if len(extracted) == 0:
            return_list.append(node)
            continue
        count = 0
        new_list = []
        for tuple in extracted:
            if count >= 1:
                image_alt = tuple[0]
                image_link = tuple[1]
                sections = new_list[-1].text.split(f"![{image_alt}]({image_link})", 1)
                if len(sections) != 2:
                    raise ValueError("Invalid markdown, image section not closed")
                new_list.pop()
                new_list.append(TextNode(sections[0], text_type_text))
                new_list.append(TextNode(image_alt, text_type_image, image_link))
                if sections[1] != "":
                    new_list.append(TextNode(sections[1], text_type_text))
                continue               
            image_alt = tuple[0]
            image_link = tuple[1]
            sections = node.text.split(f"![{image_alt}]({image_link})", 1)
            if len(sections) != 2:
                raise ValueError("Invalid markdown, image section not closed")
            new_list.append(TextNode(sections[0], text_type_text))
            new_list.append(TextNode(image_alt, text_type_image, image_link))
            if sections[1] != "":
                new_list.append(TextNode(sections[1], text_type_text))
            count += 1
        return_list.extend(new_list)
    return return_list

def split_nodes_link(old_nodes):
    return_list = []
    for node in old_nodes:
        extracted = extract_markdown_links(node.text)
        if len(extracted) == 0:
            return_list.append(node)
            continue
        count = 0
        new_list = []
        for tuple in extracted:
            if count >= 1:
                alt_text = tuple[0]
                url = tuple[1]
                sections = new_list[-1].text.split(f"[{alt_text}]({url})", 1)
                if len(sections) != 2:
                    raise ValueError("Invalid markdown, link section not closed")
                new_list.pop()
                new_list.append(TextNode(sections[0], text_type_text))
                new_list.append(TextNode(alt_text, text_type_link, url))
                if sections[1] != "":
                    new_list.append(TextNode(sections[1], text_type_text))
                continue               
            alt_text = tuple[0]
            url = tuple[1]
            sections = node.text.split(f"[{alt_text}]({url})", 1)
            if len(sections) != 2:
                raise ValueError("Invalid markdown, link section not closed")
            new_list.append(TextNode(sections[0], text_type_text))
            new_list.append(TextNode(alt_text, text_type_link, url))
            if sections[1] != "":
                new_list.append(TextNode(sections[1], text_type_text))
            count += 1
        return_list.extend(new_list)
    return return_list

def text_to_textnodes(text):
    node = TextNode(text, text_type_text)
    bold = split_nodes_delimiter([node], "**", text_type_bold)
    italic = split_nodes_delimiter(bold, "*", text_type_italic)
    code = split_nodes_delimiter(italic, "`", text_type_code)
    image = split_nodes_image(code)
    return split_nodes_link(image)
