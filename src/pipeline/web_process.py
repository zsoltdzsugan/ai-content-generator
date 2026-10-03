import requests
import os

class WebProcess:
    def __init__(self) -> None:
        self.default_download_folder = "web_sources"

    def fetch(self, url: str = "") -> (str, str):
        if not url:
            return "", "No url provided"

        response = requests.get(url, timeout=10)
        if response.status_code != 200:
            return "", f"Failed to retrieve page. Status code: {response.status_code}"

        return response.text, ""

    def download(self, text: str) -> None:
        filepath = os.path.join(self.default_download_folder, "download.html")
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(text)

        print("HTML downloaded successfully")
