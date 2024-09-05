from config import config
from openai import OpenAI
import os
import ast

_client = OpenAI()

SYSTEM_PROMPT_BASIC = """You are an expert at the video game Durb. 
Your job is to assist users with any questions they have about the game. 
Do not answer any questions or engage in conversation that is not about the game. 
The game's rules are as follows in markdown format: """
with open(os.path.join(os.path.dirname(__file__), 'game_rules.md')) as f:
    SYSTEM_PROMPT_BASIC += f.read()

class Chatbot:
    def __init__(self) -> None:
        self._api_client = _client
        self._model = config.OPENAI_MODEL
        
        self._system_prompt = SYSTEM_PROMPT_BASIC
        
        self._chat = []
        self.reset_chat()
        
    def get_chat(self) -> list[dict[str, str]]:
        return self._chat
        
    def reset_chat(self) -> None:
        self._chat = [
            {"role": "system", "content": self._system_prompt}
        ]
        
    def send_message(self, message: str):
        self._chat.append({
            "role": "user",
            "content": message
        })
        
        completion = self._api_client.chat.completions.create(
            model=self._model,
            messages=self._chat
        )
        
        response = ast.literal_eval(str(completion.choices[0].message.to_dict()))
        self._chat.append(response)
        
        return response