import time
import logging

from utils.llm import call_llm


logger = logging.getLogger("BizPilot")


class GroqAgent:

    def __init__(
        self,
        name: str,
        instruction: str
    ):

        self.name = name
        self.instruction = instruction


    def run(
        self,
        prompt: str,
        max_retries: int = 5
    ) -> str:


        full_prompt = f"""

You are {self.name}.

Your role:

{self.instruction}


User request:

{prompt}


Rules:
- Be concise
- Use clear bullet points
- Avoid unnecessary jargon
- Provide practical business recommendations
"""


        for attempt in range(max_retries):

            try:

                response = call_llm(
                    full_prompt
                )

                return response


            except Exception as e:

                logger.error(
                    f"{self.name} failed: {e}"
                )


                if attempt < max_retries - 1:

                    time.sleep(
                        2 ** attempt
                    )



        return (
            "Unable to generate response. "
            "Please try again."
        )



def create_agent(
    name,
    instruction,
    tools=None
):

    return GroqAgent(
        name,
        instruction
    )