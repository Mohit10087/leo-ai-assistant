import openai
import google.generativeai as genai

import os
import logging
import orjson
import aiofiles
import asyncio
from typing import Any, Optional, Dict


logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')


class Memory:
    def __init__(self, path: str = 'leo_memory.json'):
        self.path = path
        self.data: Dict[str, Any] = {}
        self._cache: Dict[str, Any] = {}
        # Load synchronously for initial state
        asyncio.run(self.load())

        # Setup for AI models
        self.openai_api_key = os.getenv('OPENAI_API_KEY')
        self.gemini_api_key = os.getenv('GEMINI_API_KEY')
        if self.gemini_api_key:
            genai.configure(api_key=self.gemini_api_key)
    async def smart_answer(self, prompt: str) -> str:
        """
        Generate a smart answer using the best available AI model.
        """
        # Prefer OpenAI if available
        if self.openai_api_key:
            try:
                response = await asyncio.to_thread(
                    openai.ChatCompletion.create,
                    model="gpt-4o",
                    messages=[{"role": "user", "content": prompt}],
                    api_key=self.openai_api_key
                )
                return response.choices[0].message.content.strip()
            except Exception as e:
                logging.error(f"OpenAI error: {e}")
        # Fallback to Gemini
        if self.gemini_api_key:
            try:
                model = genai.GenerativeModel('gemini-pro')
                response = await asyncio.to_thread(model.generate_content, prompt)
                return response.text.strip()
            except Exception as e:
                logging.error(f"Gemini error: {e}")
        return "AI model not available or failed."

    async def load(self) -> None:
        if os.path.exists(self.path):
            try:
                async with aiofiles.open(self.path, 'rb') as f:
                    content = await f.read()
                    self.data = orjson.loads(content)
                    self._cache = self.data.copy()
            except Exception as e:
                logging.error(f"Failed to load memory: {e}")
                self.data = {}
                self._cache = {}

    async def save(self) -> None:
        try:
            async with aiofiles.open(self.path, 'wb') as f:
                await f.write(orjson.dumps(self.data))
        except Exception as e:
            logging.error(f"Failed to save memory: {e}")


    def get(self, key: str, default: Optional[Any] = None) -> Any:
        # Use cache for fast access
        return self._cache.get(key, default)


    def set(self, key: str, value: Any) -> None:
        self.data[key] = value
        self._cache[key] = value
        asyncio.run(self.save())


    def remember_user(self, name: str, email: Optional[str] = None, preferences: Optional[dict] = None) -> None:
        self.set("user_name", name)
        if email:
            self.set("email", email)
        if preferences:
            self.set("preferences", preferences)


    def get_user_name(self) -> str:
        return self.get("user_name", "friend")


    def get_email(self) -> Optional[str]:
        return self.get("email", None)


    def get_preferences(self) -> dict:
        return self.get("preferences", {})
