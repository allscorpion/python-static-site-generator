from enum import Enum
import re

from htmlnode import HTMLNode
from parentnode import ParentNode
from textnode import TextNode, TextType, text_node_to_html_node


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


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


def extract_markdown_images(text):
    matches = re.findall(r"!\[(.*?)\]\((.*?)\)", text)

    return matches


def extract_markdown_links(text):
    matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

    return matches


def split_nodes(old_nodes, extractFn, splitStrFn, textType):
    new_list = []
    for node in old_nodes:
        if not node.textType == TextType.TEXT:
            new_list.append(node)
            continue
        matches = extractFn(node.text)

        if not len(matches):
            new_list.append(node)
            continue

        parsed_text = node.text
        for match in matches:
            full_str = splitStrFn(match)
            parts = parsed_text.split(full_str)

            if len(parts) != 2:
                raise ValueError("invalid markdown, link section not closed")

            if parts[0]:
                new_list.append(TextNode(parts[0], TextType.TEXT))
            new_list.append(TextNode(match[0], textType, match[1]))

            parsed_text = parsed_text.replace(parts[0], "")
            parsed_text = parsed_text.replace(full_str, "")

        if len(parsed_text):
            new_list.append(TextNode(parsed_text, TextType.TEXT))

    return new_list


def split_nodes_image(old_nodes):
    return split_nodes(
        old_nodes,
        extract_markdown_images,
        lambda match: f"![{match[0]}]({match[1]})",
        TextType.IMAGE,
    )


def split_nodes_link(old_nodes):
    return split_nodes(
        old_nodes,
        extract_markdown_links,
        lambda match: f"[{match[0]}]({match[1]})",
        TextType.LINK,
    )


def text_to_textnodes(text):
    new_nodes = [TextNode(text, TextType.TEXT)]

    new_nodes = split_nodes_delimiter(new_nodes, "**", TextType.BOLD)
    new_nodes = split_nodes_delimiter(new_nodes, "_", TextType.ITALIC)
    new_nodes = split_nodes_delimiter(new_nodes, "`", TextType.CODE)
    new_nodes = split_nodes_link(new_nodes)
    new_nodes = split_nodes_image(new_nodes)

    return new_nodes


def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    new_blocks = []

    for block in blocks:
        parsed_block = block.strip()

        if not parsed_block:
            continue

        lines = parsed_block.split("\n")

        output = []

        for line in lines:
            output.append(line.strip())

        new_blocks.append("\n".join(output))

    return new_blocks


def block_to_block_type(block):
    if re.match(r"^#{1,6} (.+)", block):
        return BlockType.HEADING

    if re.match(r"^```([\s\S]+)```$", block):
        return BlockType.CODE

    lines = block.split("\n")
    quoteMatches = 0
    unorderedListMatches = 0
    orderedListMatches = 0
    orderedListNum = 1

    for line in lines:
        if re.match(r"^>(.*)", line):
            quoteMatches += 1
        elif re.match(r"^- (.+)", line):
            unorderedListMatches += 1
        else:
            numberMatch = re.findall(r"^([0-9]). (.+)", line)
            if numberMatch and int(numberMatch[0][0]) == orderedListNum:
                orderedListNum += 1
                orderedListMatches += 1

    total_lines = len(lines)

    if quoteMatches == total_lines:
        return BlockType.QUOTE

    if unorderedListMatches == total_lines:
        return BlockType.UNORDERED_LIST

    if orderedListMatches == total_lines:
        return BlockType.ORDERED_LIST

    return BlockType.PARAGRAPH


def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    html_nodes = []
    for block in blocks:
        blockType = block_to_block_type(block)

        match blockType:
            case BlockType.PARAGRAPH:
                block = block.replace("\n", " ")
                child_nodes = []
                text_nodes = text_to_textnodes(block)

                for text_node in text_nodes:
                    html_node = text_node_to_html_node(text_node)
                    child_nodes.append(html_node)

                html_nodes.append(ParentNode("p", child_nodes))

            case BlockType.QUOTE:
                lines = block.split("\n")
                new_lines = []
                for line in lines:
                    parsed_line = line.replace(">", "").strip()

                    if not parsed_line:
                        continue

                    new_lines.append(parsed_line)

                parsed_block = " ".join(new_lines)

                child_nodes = []
                text_nodes = text_to_textnodes(parsed_block)

                for text_node in text_nodes:
                    html_node = text_node_to_html_node(text_node)
                    child_nodes.append(html_node)

                html_nodes.append(ParentNode("blockquote", child_nodes))

            case BlockType.UNORDERED_LIST:
                lines = block.split("\n")
                list_nodes = []
                for line in lines:
                    child_nodes = []
                    text_nodes = text_to_textnodes(line.replace("- ", ""))
                    for text_node in text_nodes:
                        html_node = text_node_to_html_node(text_node)
                        child_nodes.append(html_node)

                    list_nodes.append(ParentNode("li", child_nodes))

                html_nodes.append(ParentNode("ul", list_nodes))

            case BlockType.ORDERED_LIST:
                lines = block.split("\n")
                list_nodes = []
                for line in lines:
                    child_nodes = []
                    matches = re.match(r"^([0-9]). (.+)", line)

                    if not matches:
                        continue

                    text_nodes = text_to_textnodes(matches[2])
                    for text_node in text_nodes:
                        html_node = text_node_to_html_node(text_node)
                        child_nodes.append(html_node)

                    list_nodes.append(ParentNode("li", child_nodes))

                html_nodes.append(ParentNode("ol", list_nodes))

            case BlockType.HEADING:
                block = block.replace("\n", " ")
                match = re.match(r"^(#{1,6}) (.+)", block)

                if not match:
                    continue

                heading_el = len(match[1])
                text = match[2]

                child_nodes = []
                text_nodes = text_to_textnodes(text)
                for text_node in text_nodes:
                    html_node = text_node_to_html_node(text_node)
                    child_nodes.append(html_node)

                html_nodes.append(ParentNode(f"h{heading_el}", child_nodes))

            case BlockType.CODE:
                child_nodes = []
                text_nodes = [
                    TextNode(
                        block.replace("```\n", "").replace("```", ""),
                        TextType.CODE,
                    )
                ]

                for text_node in text_nodes:
                    html_node = text_node_to_html_node(text_node)
                    child_nodes.append(html_node)

                html_nodes.append(ParentNode("pre", child_nodes))

    return ParentNode("div", html_nodes)


def extract_title(markdown):
    blocks = markdown_to_blocks(markdown)

    for block in blocks:
        blockType = block_to_block_type(block)

        if blockType == BlockType.HEADING:
            match = re.match(r"^(#{1}) (.+)", block)
            if not match:
                continue

            return match[2]

    raise Exception("no h1 header found")
