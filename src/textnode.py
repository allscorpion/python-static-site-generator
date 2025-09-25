from enum import Enum


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
