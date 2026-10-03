import os
import json
from openai import OpenAI
from dotenv import load_dotenv
from system_prompt import system_prompt
from models.research import Research
from models.source import Source

class LLMProcess:
    def get_response(self, research: Research, user_prompt: str = "") -> str:
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
        ]
        user_instructions = f"Article's topic: {research.query}\n\n"

        if len(user_prompt) != 0:
            user_instructions = f"Additional user instructions: {user_prompt}\n\n"
        
        if len(research.sources) != 0:
            user_instructions += self.sources_to_prompt(research.sources)
            source_msg = { "role": "user", "content": user_instructions }
            messages.append(source_msg)

        response = client.chat.completions.create(model="openrouter/free", messages=messages)
        message = response.choices[0].message
        messages.append(message)

        return message.content

    def generate_markdown(self, research: Research, user_prompt: str = "") -> str:
        markdown = self.get_response(research, user_prompt)
        
        return markdown

    def sources_to_prompt(self, sources: list[Source]) -> str:
        if not sources:
            return ""
        sources_list : list[str] = []
        for source in sources:
            sources_list.append(f"""
        --- SOURCE ---
        Title: {source.title}
        URL: {source.url}
        Type: {source.type.value}

        Content:
        {source.content}
        --- END SOURCE ---
        """)

        return "\n\n".join(sources_list)
