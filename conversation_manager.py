from openai import OpenAI
import tiktoken
import json
from datetime import datetime
import os

class ConversationManager:
    def __init__(self, api_key, base_url="https://api.openai.com/v1", history_folder="Past_Conversations", history_file=None):
        self.client = OpenAI(api_key=api_key)
        self.base_url = base_url
        self.default_max_tokens = 1000
        self.token_budget = 4000
        self.default_model = "gpt-3.5-turbo"
        self.default_temperature = 0.8
        self.system_message = "Ask me anything!"

        if not os.path.exists(history_folder):
            os.makedirs(history_folder)
        
        if history_file is None:
            timestamp = datetime.now().strftime("%m%d%y_%H%M%S")
            self.history_file = os.path.join(history_folder, f"conversation_history_{timestamp}.json")
        else:
            self.history_file = os.path.join(history_folder, history_file)

        self.load_conversation_history()

    def count_tokens(self, text):
        encoding = tiktoken.encoding_for_model(self.default_model)
        tokens = encoding.encode(text)
        return len(tokens)

    def total_tokens_used(self):
        try:
            total = 0
            for message in self.conversation_history:
                total += self.count_tokens(message["content"])
            return total
        
        except Exception as e:
            print(f"An unexpected error occurred while calculating the total tokens used: {e}")
            return None

    def enforce_token_budget(self):
        try:
            while self.total_tokens_used() > self.token_budget:
                if len(self.conversation_history) <= 1:
                    break
                self.conversation_history.pop(1)
            
        except Exception as e:
            print(f"An unexpected error occurred while enforcing the token budget: {e}")

    def update_system_message_in_history(self):
        try:
            if self.conversation_history and self.conversation_history[0]["role"] == "system":
                self.conversation_history[0]["content"] = self.system_message
            else:
                self.conversation_history.insert(0, {"role": "system", "content": self.system_message})

        except Exception as e:
            print(f"An unexpected error occurred while updating the system message in the conversation history: {e}")

    def chat_completion(self, prompt, temperature=None, max_tokens=None, model=None):
        temperature = temperature if temperature is not None else self.default_temperature
        max_tokens = max_tokens if max_tokens is not None else self.default_max_tokens
        model = model if model is not None else self.default_model

        self.conversation_history.append({"role": "user", "content": prompt})
        self.enforce_token_budget()

        try:
            response = self.client.chat.completions.create(
                model=model,
                messages=self.conversation_history,
                temperature=temperature,
                max_tokens=max_tokens,
            )
        
        except Exception as e:
            print(f"An error occurred while generating a response: {e}")
            return None
        
        ai_response = response.choices[0].message.content
        self.conversation_history.append({"role": "assistant", "content": ai_response})
        self.save_conversation_history()

        return ai_response

    def load_conversation_history(self):
        try:
            with open(self.history_file, "r") as file:
                self.conversation_history = json.load(file)

        except FileNotFoundError:
            self.conversation_history = [{"role": "system", "content": self.system_message}]
        
        except json.JSONDecodeError:
            print("Error reading the conversation history file. Starting with an empty history.")
            self.conversation_history = [{"role": "system", "content": self.system_message}]
    
    def save_conversation_history(self):
        try:
            with open(self.history_file, "w") as file:
                json.dump(self.conversation_history, file, indent=4)
        
        except Exception as e:
            print(f"An unexpected error occurred while saving the conversation history: {e}")
    
    def reset_conversation_history(self):
        self.conversation_history = [{"role": "system", "content": self.system_message}]
        try:
            # Attempt to save the reset history to the file
            self.save_conversation_history()
        
        except Exception as e:
            print(f"An unexpected error occurred while resetting the conversation history: {e}")
