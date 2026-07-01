import json

class LLMAgent:
    def __init__(self, name, llm_call):
        self.name = name
        self.llm_call = llm_call

    def run(self, prompt: str):
        response = self.llm_call(prompt)

        return {
            "agent": self.name,
            "input": prompt,
            "output": response
        }