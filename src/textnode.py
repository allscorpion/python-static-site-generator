from enum import Enum

from leafnode import LeafNode


class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"


class TextNode:
    def __init__(self, text, textType: TextType, url=None):
        self.text = text
        self.textType = textType
        self.url = url

    def __eq__(self, other):
        return (
            self.text == other.text
            and self.textType == other.textType
            and self.url == other.url
        )

    def __repr__(self) -> str:
        return f"TextNode({self.text}, {self.textType.value}, {self.url})"


def text_node_to_html_node(text_node: TextNode):
    match text_node.textType:
        case TextType.TEXT:
            return LeafNode(None, text_node.text)
        case TextType.BOLD:
            return LeafNode("b", text_node.text)
        case TextType.ITALIC:
            return LeafNode("i", text_node.text)
        case TextType.LINK:
            return LeafNode("a", text_node.text, {"href": text_node.url})
        case TextType.IMAGE:
            return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
        case TextType.CODE:
            return LeafNode("code", text_node.text)
        case _:
            raise Exception(f"unsupported text type {text_node.textType}")
