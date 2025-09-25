from textnode import TextNode, TextType


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_list = []
    for node in old_nodes:
        if not node.textType == TextType.TEXT:
            new_list.append(node)
            continue
        if delimiter in node.text:
            text_parts = node.text.split(delimiter)

            if len(text_parts) % 2 == 0:
                raise Exception("no closing delimiter found")

            for i in range(len(text_parts)):
                part = text_parts[i]

                if part == "":
                    continue

                if (i + 1) % 2 == 0:
                    new_list.append(TextNode(part, text_type))
                else:
                    new_list.append(TextNode(part, TextType.TEXT))
        else:
            new_list.append(node)
    return new_list
