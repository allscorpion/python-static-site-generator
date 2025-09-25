import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_links(self):
        node = TextNode("This is a link node", TextType.LINK, "https://www.google.com")
        node2 = TextNode("This is a link node", TextType.LINK, "https://www.google.com")
        self.assertEqual(node, node2)

    def test_links_with_different_url(self):
        node = TextNode("This is a link node", TextType.LINK, "https://www.youtube.com")
        node2 = TextNode("This is a link node", TextType.LINK, "https://www.google.com")
        self.assertNotEqual(node, node2)

    def test_different_types(self):
        node = TextNode("This is a node", TextType.BOLD)
        node2 = TextNode("This is a node", TextType.CODE)
        self.assertNotEqual(node, node2)

    def test_manual_link(self):
        node = TextNode("This is a node", TextType.BOLD, None)
        node2 = TextNode("This is a node", TextType.BOLD, None)
        self.assertEqual(node, node2)


if __name__ == "__main__":
    unittest.main()
