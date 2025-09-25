import unittest

from htmlnode import HTMLNode


class TestHtmlNode(unittest.TestCase):
    def test_p(self):
        node = HTMLNode("p", "This is a text node")
        node2 = HTMLNode("p", "This is a text node")
        self.assertEqual(node, node2)

    def test_empty(self):
        node = HTMLNode()
        node2 = HTMLNode()
        self.assertEqual(node, node2)

    def test_all_props(self):
        node = HTMLNode("div", "This is the text inside my div", None, None)
        node2 = HTMLNode("div", "This is the text inside my div", None, None)
        self.assertEqual(node, node2)

    def test_link_props(self):
        node = HTMLNode(
            "a",
            "This is the text inside my a",
            None,
            {"href": "https://www.google.com"},
        )

        expected = f'href="https://www.google.com"'

        self.assertEqual(node.props_to_html(), expected)

    def test_multiple_props(self):
        node = HTMLNode(
            "a",
            "This is the text inside my a",
            None,
            {"href": "https://www.google.com", "class": "button"},
        )

        expected = f'href="https://www.google.com" class="button"'

        self.assertEqual(node.props_to_html(), expected)


if __name__ == "__main__":
    unittest.main()
