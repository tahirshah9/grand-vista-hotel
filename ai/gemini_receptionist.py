import google.generativeai as genai

class GeminiReceptionist:
    def __init__(self, api_key: str):
        genai.configure(api_key=api_key)
        self.__model = genai.GenerativeModel("gemini-2.0-flash")
        self.__history = []
        self.__system_prompt = "You are Aria, a professional hotel receptionist at Grand Vista Hotel. Be concise, polite, and helpful."

    def chat(self, user_message: str, context: str = "") -> str:
        try:
            full_prompt = f"{self.__system_prompt}\n\nHotel Context:\n{context}\n\nGuest: {user_message}"
            # Inject history if needed, but for simplicity we append to prompt or just maintain context.
            # To do proper multi-turn we can format the history into the prompt.
            history_text = "\n".join([f"Guest: {h['user']}\nAria: {h['aria']}" for h in self.__history[-5:]])
            if history_text:
                full_prompt = f"{self.__system_prompt}\n\nHotel Context:\n{context}\n\nRecent Chat History:\n{history_text}\n\nGuest: {user_message}\nAria:"

            response = self.__model.generate_content(full_prompt)
            self.__history.append({"user": user_message, "aria": response.text})
            return response.text
        except Exception as e:
            return f"I'm sorry, I'm having trouble right now. ({str(e)})"

    def reset_conversation(self):
        self.__history = []
