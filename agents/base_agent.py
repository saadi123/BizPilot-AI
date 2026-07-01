import os
import time
import requests
import json

class GroqAgent:
    def __init__(self, name: str, instruction: str):
        self.name = name
        self.instruction = instruction

    def run(self, prompt: str, max_retries: int = 5) -> str:
        api_key = os.environ.get("GROQ_API_KEY")
        if not api_key:
            from utils.llm import call_llm
            return f"[Simulated response for {self.name}]: {call_llm(prompt)}"

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        }

        system_content = self.instruction
        if "ONLY valid JSON" not in self.instruction and "Output ONLY valid JSON" not in self.instruction:
            system_content += "\n\nCRITICAL INSTRUCTION: Keep your response extremely concise. Use short sentences, clear bullet points, and avoid long paragraphs. Use layman's terms and avoid complex legal or financial jargon so that it is easily understood by someone without a finance background."

        data = {
            "model": "llama-3.1-8b-instant",
            "messages": [
                {"role": "system", "content": system_content},
                {"role": "user", "content": prompt}
            ]
        }

        for attempt in range(max_retries):
            try:
                response = requests.post("https://api.groq.com/openai/v1/chat/completions", headers=headers, json=data)
                response.raise_for_status()
                result = response.json()
                return result["choices"][0]["message"]["content"]
            except Exception as e:
                status_code = getattr(getattr(e, 'response', None), 'status_code', None)
                if "429" in str(e) or status_code == 429:
                    if attempt < max_retries - 1:
                        time.sleep((2 ** attempt) * 2)
                        continue
                if attempt == max_retries - 1:
                    return f"[Error from Groq API for {self.name}]: {str(e)} - {response.text if 'response' in locals() else ''}"
        
        return "No response"

def create_agent(
    name,
    instruction,
    tools=None
):
    return GroqAgent(name, instruction)