from ..config import config
from openai import OpenAI

client = OpenAI()

SYSTEM_PROMPT_BASIC = "You are an expert at the video game Durb. Your job is to assist users with any questions they have about the game. The game's rules are as follows in markdown format: "

class Chatbot:
    def __init__(self) -> None:
        self._api_client = OpenAI()
        self._model = config.OPENAI_MODEL
        
        self._system_prompt = SYSTEM_PROMPT_BASIC
        with open('game_rules.md') as f:
            self._system_prompt += f.read()
            
        self._chat = []
        self.reset_chat()
        
    def get_chat(self) -> list[dict[str, str]]:
        return self._chat
        
    def reset_chat(self) -> None:
        self._chat = [
            {"role": "system", "content": self._system_prompt}
        ]
        
    def send_message(self, message: str) -> str:
        self._chat.append({
            "role": "user",
            "content": message
        })
        
        completion = self._api_client.chat.completions.create(
            model=self._model,
            messages=self._chat
        )
        
        response = completion.choices[0].message
        self._chat.append({
            "role": "assistant",
            "content": response
        })
        
        return response