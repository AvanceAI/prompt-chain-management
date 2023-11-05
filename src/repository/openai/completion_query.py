from dotenv import load_dotenv
load_dotenv()

import os
import openai

openai.api_key = os.environ['OPENAI_API_KEY']

class CompletionQuery:
    def __init__(self, model, temperature, max_tokens, top_p=1, frequency_penalty=0):
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.top_p = top_p
        self.frequency_penalty = frequency_penalty

    def run(self, prompt, print=False):
        if print:
            print('////////////')
            print(f"message to be sent: {prompt}")
            print('************')
            print('************')
        response = openai.Completion.create(
        model=self.model,
        prompt=prompt,
        temperature=self.temperature,
        max_tokens=self.max_tokens,
        top_p=self.top_p,
        frequency_penalty=self.frequency_penalty,
        presence_penalty=0,
        stop=["|||"]
        )
        result = response["choices"][0]["text"]
        
        if print:
            print('////////////')
            print(f"response content: {result}")
            print('************')
            print('************')
        return result