import unittest

from split_nodes_delimiter import split_nodes_delimiter
from textnode import TextNode, TextType


class Test(unittest.TestCase):
    def test_code_block(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)

        self.assertListEqual(
            new_nodes,
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" word", TextType.TEXT),
            ],
        )

    def test_code_block_2(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node, node], "`", TextType.CODE)

        self.assertListEqual(
            new_nodes,
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" word", TextType.TEXT),
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" word", TextType.TEXT),
            ],
        )

    def test_bold_block(self):
        node = TextNode("This is text with a **code block** word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)

        self.assertListEqual(
            new_nodes,
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("code block", TextType.BOLD),
                TextNode(" word", TextType.TEXT),
            ],
        )

    def test_bold_block_2(self):
        new_nodes = split_nodes_delimiter(
            [
                TextNode("This is text", TextType.TEXT),
                TextNode("This is text with a **code block** word", TextType.TEXT),
            ],
            "**",
            TextType.BOLD,
        )

        self.assertListEqual(
            new_nodes,
            [
                TextNode("This is text", TextType.TEXT),
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("code block", TextType.BOLD),
                TextNode(" word", TextType.TEXT),
            ],
        )

    def test_no_matching_close(self):

        self.assertRaises(
            Exception,
            lambda: split_nodes_delimiter(
                [
                    TextNode("This is text with a **code block word", TextType.TEXT),
                ],
                "**",
                TextType.BOLD,
            ),
        )

    def test_delim_bold_and_italic(self):
        node = TextNode("**bold** and _italic_", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        new_nodes = split_nodes_delimiter(new_nodes, "_", TextType.ITALIC)
        self.assertListEqual(
            [
                TextNode("bold", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
            ],
            new_nodes,
        )

    def test_delim_bold_multiword(self):
        node = TextNode(
            "This is text with a **bolded word** and **another**", TextType.TEXT
        )
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bolded word", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("another", TextType.BOLD),
            ],
            new_nodes,
        )


if __name__ == "__main__":
    unittest.main()
