from htmlnode import HTMLNode


class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if not self.value:
            raise ValueError("All leaf nodes must have a value.")

        if not self.tag:
            return self.value

        if self.props:
            string_props = self.props_to_html()
            return f"<{self.tag} {string_props}>{self.value}</{self.tag}>"

        return f"<{self.tag}>{self.value}</{self.tag}>"
