import os
import json
from datetime import datetime, UTC
from openai import OpenAI
from dotenv import load_dotenv
from models.research import Research
from models.source import Source, SourceType
from pipeline.web_process import WebProcess
from pipeline.html_process import HTMLProcess

class ResearchProcess:
    def run(self, topic: str, url: str, prompt: str = "") -> None:
        research = Research(topic)
        research.start()

        web_process = WebProcess()
        html_text, err = web_process.fetch(url)
        if err:
            raise Exception(err)
        web_process.download(html_text)

        html_process = HTMLProcess()
        source = html_process.html_to_source(url, html_text)
        research.add_source(source)

        research.complete()

    def get_response(self):
        load_dotenv()
        api_key = os.environ.get("OPENROUTER_API_KEY")

        if api_key is None:
            raise RuntimeError("Missing or wrong api key!")

        client = OpenAI(
           base_url="https://openrouter.ai/api/v1",
           api_key=api_key,
        )

        messages = [
            { "role": "system", "content": system_prompt },
            { "role": "user", "content": args.user_prompt },
        ]

        response = client.chat.completions.create(model="openrouter/free", messages=messages)
        message = response.choices[0].message
        messages.append(message)
