from htmlnode import HTMLNode


class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if not self.tag:
            raise ValueError("tag is required")

        if not self.children:
            raise ValueError("children is required")

        output_str = f"<{self.tag}"

        if self.props:
            props_str = self.props_to_html()
            output_str += f" {props_str}"

        output_str += ">"

        for child in self.children:
            output_str += child.to_html()

        output_str += f"</{self.tag}>"
        return output_str
