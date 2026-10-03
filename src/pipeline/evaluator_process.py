import os
import json
from urllib.parse import urlparse
from models.source import Source

class EvaluatorProcess:
    def __init__(self, threshold: float = 0.3) -> None:
        self.threshold: float = threshold
        self.default_folder: str = "web_sources"

    def evaluate(self, sources: list[Source]) -> tuple[list[Source], list[str]]:
        rep_dict: dict = self.load_reputation()

        ok_sources: list[Source] = []
        for source in sources:
            domain = self.get_domain(source.url)
            if domain not in rep_dict:
                rep_dict[domain] = {}
                rep_dict[domain]["evaluated_sources"] = 1
                rep_dict[domain]["total_score"] = source.score
                rep_dict[domain]["is_excluded"] = False
            else:
                if rep_dict[domain]["is_excluded"]:
                    continue
                rep_dict[domain]["evaluated_sources"] += 1
                rep_dict[domain]["total_score"] += source.score
                average_score = rep_dict[domain]["total_score"] / rep_dict[domain]["evaluated_sources"]

                if rep_dict[domain]["evaluated_sources"] >= 5 and average_score < self.threshold:
                    rep_dict[domain]["is_excluded"] = True
                    continue
            ok_sources.append(source)

        excluded_domains: list[str] = []
        for domain, reputation in rep_dict.items():
            if reputation["is_excluded"]:
                excluded_domains.append(domain)

        self.save_reputation(rep_dict)

        return ok_sources, excluded_domains

    def load_reputation(self) -> dict:
        filepath = os.path.join(self.default_folder, "source_reputation.json")
        basedir = os.path.dirname(filepath)

        if not os.path.exists(basedir):
            os.mkdir(self.default_folder)

        if not os.path.exists(filepath):
            return {}

        with open(filepath, 'r', encoding='utf-8') as f:
            content: str = f.read().strip()

            if not content:
                return {}

            return json.loads(content)

    def save_reputation(self, data: dict) -> None:
        filepath = os.path.join(self.default_folder, "source_reputation.json")
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4)

    def get_domain(self, url: str) -> str:
        if len(url) == 0:
            return ""

        parsed_url = urlparse(url)
        if parsed_url.hostname is None:
            return ""

        domain = parsed_url.hostname

        if domain.startswith("www."):
            domain = domain[4:]

        return domain
