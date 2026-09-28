from bs4 import BeautifulSoup
from models.source import *

class HTMLProcess:
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
