import os
import json
from datetime import datetime, UTC
from openai import OpenAI
from dotenv import load_dotenv
from models.research import Research

class ResearchProcess:
    def __init__(self) -> None:
        self.created_at: datetime = datetime.now(UTC)
        self.finished_at: datetime | None = None

    def run(self, topic: str, prompt: str) -> None:
        if not topic:
            raise Exception("No topic provided")

        research = Research(topic)
        research.start()

        #response = self.get_response()

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
