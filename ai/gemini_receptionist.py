import os
from google import genai
from google.genai import types

class GeminiReceptionist:
    def __init__(self, api_key: str):
        self.client = genai.Client(api_key=api_key)
        self.__model = "gemini-2.5-flash"
        self.__history = []
        self.__system_prompt = "You are Aria, a professional hotel receptionist at Grand Vista Hotel. Be concise, polite, and helpful."

    def chat(self, user_message: str, context: str = "") -> str:
        try:
            full_prompt = f"Hotel Context:\n{context}\n\nGuest: {user_message}"
            
            history_text = "\n".join([f"Guest: {h['user']}\nAria: {h['aria']}" for h in self.__history[-5:]])
            if history_text:
                full_prompt = f"Hotel Context:\n{context}\n\nRecent Chat History:\n{history_text}\n\nGuest: {user_message}\nAria:"

            response = self.client.models.generate_content(
                model=self.__model,
                contents=full_prompt,
                config=types.GenerateContentConfig(
                    system_instruction=self.__system_prompt,
                ),
            )
            self.__history.append({"user": user_message, "aria": response.text})
            return response.text
        except Exception as e:
            return f"I'm sorry, I'm having trouble right now. ({str(e)})"

    def reset_conversation(self):
        self.__history = []

