from dotenv import load_dotenv
load_dotenv()

import os
import json
import ast
import openai
openai.api_key = os.environ['OPENAI_API_KEY']

class Query:
    def __init__(self, model, temperature, max_tokens, top_p=1, frequency_penalty=0, system_message=None) -> None:
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.top_p = top_p
        self.frequency_penalty = frequency_penalty
        self.messages = []
        if system_message:
            self.messages.append({"role": "system", "content": system_message})
            print('////////////')
            print("system message: ", system_message)
            print('************')
            print('************')
     
    def send_message(self, message: str):
        print('////////////')
        print(f"message to be sent: {message}")
        print('************')
        print('************')
        self.messages.append({"role": "user", "content": message})
        response = self._send(messages=self.messages)
        chatbot_response = response["choices"][0]["message"].to_dict()
        print('////////////')
        print(f"response content: {chatbot_response['content']}")
        print('************')
        print('************')
        self.messages.append(chatbot_response)
        return chatbot_response["content"]
        
    def _send(self, messages):
        response = openai.ChatCompletion.create(
        model=self.model,
        messages=messages,
        temperature=self.temperature,
        max_tokens=self.max_tokens,
        top_p=self.top_p,
        frequency_penalty=self.frequency_penalty,
        presence_penalty=0.0,
        stop=["|||"]
        )
        return response
    
    def run_with_data_or_prompt(self, prompt=None,  data=None):
        if isinstance(data, dict):
            data = json.dumps(data, indent=4)
        elif isinstance(data, list):
            data = str(data)
        else:
            pass
        
        if data is None:
            message = prompt
        elif prompt is not None and data is not None:
            message = prompt + '\n\n\n\n' + data
        else:
            message = data
        res = self.send_message(message=message)
        return res
    
    def run(self, prompt=None, data=None, eval_literal=True):
        if prompt is None and data is None:
            chatbot_response = self._send(messages=self.messages)["choices"][0]["message"].to_dict()
            self.messages.append(chatbot_response)
            res = chatbot_response["content"]
        else:
            res = self.run_with_data_or_prompt(prompt=prompt, data=data)
        
        if eval_literal:
            res = ast.literal_eval(res)
        return res
