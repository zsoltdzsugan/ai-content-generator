import os
import json
from dotenv import load_dotenv
from tavily import TavilyClient
from models.source import Source, SourceType

class SearchProcess:
    def get_sources(self, query: str = "", topic: str = "", exclude_domains: list[str] = []) -> list[Source]:
        client = self.setup_client()
        if topic:
            response = client.search(query=query, topic=topic, max_results=10, search_depth="advanced", include_published_date=True, exclude_domains=exclude_domains)
        else:
            response = client.search(query=query, max_results=10, search_depth="advanced", include_published_date=True, exclude_domains=exclude_domains)

        if not response["results"]:
            return []

        match (topic.lower()):
            case "news":
                source_type = SourceType.NEWS
            case _:
                source_type = SourceType.GENERAL

        sources = []
        for result in response["results"]:
            source = Source(result["title"], result["url"], source_type, result["content"], result["score"])
            sources.append(source)

        return sources

    def setup_client(self) -> TavilyClient:
        load_dotenv()

        api_key = os.environ.get("TAVILY_API_KEY")
        if api_key is None:
            raise RuntimeError("Missing or wrong api key")

        client = TavilyClient(api_key)
        if not client:
            raise RuntimeError("No API client")

        return client
