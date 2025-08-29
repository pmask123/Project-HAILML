from pydantic import BaseModel, Field


class Pipe:
    class Valves(BaseModel):
        """
        Variables to configure the Pipe
        """

        MODEL_ID: str = Field(default="")

    def __init__(self):
        self.valves = self.Valves()

    def pipe(self, body: dict):
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
        # Logic goes here
        print(
            self.valves, body
        )  # This will print the configuration options and the input body
        return "Hello, World!"
