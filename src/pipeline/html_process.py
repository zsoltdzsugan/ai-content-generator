import os
from bs4 import BeautifulSoup
from pipeline.markdown_process import MarkdownProcess
from models.source import *
from models.html.leafnode import LeafNode
from models.html.parentnode import ParentNode

class HTMLProcess:
    def generate_index(self, basepath="/") -> None:
        content_dir_path: str = "content/blog"
        dest_path: str = "docs/index.html"

        if not os.path.exists(content_dir_path):
            raise Exception("Content path does not exists")

        md_process: MarkdownProcess = MarkdownProcess()
        list_items: list[HTMLNode] = []

        for filename in os.listdir(content_dir_path):
            if not filename.endswith(".md"):
                continue

            source_path: str = os.path.join(content_dir_path, filename)

            if not os.path.isfile(source_path):
                continue

            with open(source_path, "r") as f:
                markdown: str = f.read()

            title: str = md_process.extract_title(markdown)
            html_filename: str = filename.removesuffix(".md") + ".html"

            link: LeafNode = LeafNode("a", title, {"href": f"blog/{html_filename}"})
            list_items.append(ParentNode("li", [link]))

        ul: ParentNode = ParentNode("ul", list_items)

        os.makedirs(os.path.dirname(dest_path), exist_ok=True)

        with open(dest_path, "r") as f:
            index_content = f.read()

        html: str = index_content.replace("{{ ArticleLinks }}", ul.to_html())
        html = html.replace('href="/', f'href="{basepath}')
        html = html.replace('src="/', f'src="{basepath}')

        with open(dest_path, "w") as f:
            f.write(html)

    def generate_page(self, from_path, template_path, dest_path, basepath="/", markdown_process: MarkdownProcess | None = None) -> None:
        #print(f"Generating page from {from_path} to {dest_path} using {template_path}")

        if markdown_process is None:
            raise RuntimeError("MarkdownProcess is none")

        with open(from_path, 'r') as f:
            from_contents = f.read()

        with open(template_path, 'r') as f:
            template_contents = f.read()

        title: str = markdown_process.extract_title(from_contents)
        from_html_node: HTMLNode = markdown_process.markdown_to_html_node(from_contents)
        content: str = from_html_node.to_html()
        
        html: str = template_contents.replace("{{ Title }}", title)
        html = html.replace("{{ Content }}", content)
        html = html.replace('href="/', f'href="{basepath}')
        html = html.replace('src="/', f'src="{basepath}')

        dest_dir = os.path.dirname(dest_path)
        if dest_dir != "":
            os.makedirs(dest_dir, exist_ok=True)
        
        with open(dest_path, "w") as f:
            f.write(html)

    def generate_pages_recursive(self, dir_path_content, template_path, dest_dir_path, basepath="/"):
        if not os.path.exists(dir_path_content):
            raise Exception("Content path not exists")

        md_process: MarkdownProcess = MarkdownProcess()
        for item in os.listdir(dir_path_content):
            source_path = os.path.join(dir_path_content, item)
            dest_path = os.path.join(dest_dir_path, item)

            if os.path.isdir(source_path):
                os.makedirs(dest_path, exist_ok=True)

                self.generate_pages_recursive(source_path, template_path, dest_path, basepath)

            elif os.path.isfile(source_path):
                if not item.endswith(".md"):
                    continue

                dest_path = os.path.splitext(dest_path)[0] + ".html"
                self.generate_page(source_path, template_path, dest_path, basepath, md_process)



    ### OLD FEATURES
    # intended for fallback if search engine fails
    def parse_html(self, raw_html: str) -> dict:
        soup = BeautifulSoup(raw_html, features="html.parser")
        html: dict = {}

        html["title"] = soup.title.string
        if soup.find("article"):
            html["content"] = list(soup.find("article").stripped_strings)
        else:
            html["content"] = list(soup.body.stripped_strings)

        return html

    def html_to_source(self, url: str, raw_html_str: str) -> Source:
        html = self.parse_html(raw_html_str)

        title = html["title"]
        content = "\n".join(html["content"])

        return Source(title, url, SourceType.NEWS, content)
