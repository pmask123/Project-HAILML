from pydantic import BaseModel, Field
import requests


class Pipe:
    """
    Phi-4 Translation Pipeline
    """

    class Valves(BaseModel):
        """
        Variables to configure the Pipe
        """

        ENDPOINT: str = Field(
            default="http://127.0.0.1:8000/",
            description="HTTP endpoint for hosted model",
        )
        SYSTEM_PROMPT: str = Field(
            default="Translate the following user input into Italian",
            description="Model system prompt for translating user input.",
        )

    def __init__(self):
        self.valves = self.Valves()

    def pipe(self, body: dict) -> str:
        """
        Main Open WebUI pipeline function.

         - Processes input messages
         - Gets model response
         - Parses model response and outputs

        Args:
            body (dict): Open WebUI body, e.g.
                {
                    "stream": True,
                    "model": "test2",
                    "messages": [{"role": "user", "content": "hello there how are you"}],
                }

        Returns:
            str: model response
        """

        user_prompt = body["messages"][-1]["content"]  # latest user message

        payload = dict(
            system_prompt=self.valves.SYSTEM_PROMPT, user_prompt=user_prompt
        )  # see schemas.model_schemas.PhiInput

        response = requests.post(self.valves.ENDPOINT, json=payload)

        return response.text
