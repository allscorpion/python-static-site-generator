import unittest

from leafnode import LeafNode
from parentnode import ParentNode


class TestParentNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_multi_nested(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode(
            "span",
            [
                ParentNode("div", [grandchild_node]),
            ],
        )
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><div><b>grandchild</b></div></span></div>",
        )

    def test_no_children(self):
        child_node = ParentNode(
            "span",
            [],
        )
        parent_node = ParentNode("div", [child_node])
        self.assertRaises(
            ValueError,
            parent_node.to_html,
        )


if __name__ == "__main__":
    unittest.main()
