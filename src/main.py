import os
import re
import shutil

from markdown import extract_title, markdown_to_html_node


def copy_dir(dir, path, dest):
    for item in dir:
        full_path = os.path.join(path, item)
        is_file = os.path.isfile(full_path)

        if is_file:
            shutil.copy(full_path, dest)
            continue

        dest_folder = os.path.join(dest, full_path.replace("./static/", ""))
        if not os.path.exists(dest_folder):
            os.mkdir(dest_folder)
        copy_dir(os.listdir(full_path), full_path, dest_folder)


def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    with open(from_path) as f:
        file_contents = f.read()

        with open(template_path) as t:
            template_contents = t.read()

            html_nodes = markdown_to_html_node(file_contents)
            title = extract_title(file_contents)

            template_contents = template_contents.replace("{{ Title }}", title)
            template_contents = template_contents.replace(
                "{{ Content }}", html_nodes.to_html()
            )

            with open(dest_path, "x") as d:
                d.write(template_contents)


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    dir = os.listdir(dir_path_content)

    for item in dir:
        full_path = os.path.join(dir_path_content, item)
        is_file = os.path.isfile(full_path)

        if is_file:
            if not ".md" in item:
                raise Exception("cannot handle non markdown files")

            generate_page(
                full_path,
                template_path,
                os.path.join(dest_dir_path, item.replace(".md", ".html")),
            )
            continue

        dest_folder = os.path.join(dest_dir_path, item)

        if not os.path.exists(dest_folder):
            os.mkdir(dest_folder)
        generate_pages_recursive(full_path, template_path, dest_folder)


def main():
    public_dir = "./public"
    static_dir = "./static"
    public_exists = os.path.exists(public_dir)

    if public_exists:
        shutil.rmtree(public_dir)

    os.mkdir(public_dir)
    dir = os.listdir(static_dir)

    copy_dir(dir, static_dir, public_dir)

    generate_pages_recursive("./content", "./template.html", "./public")


if __name__ == "__main__":
    main()
