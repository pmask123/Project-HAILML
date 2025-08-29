# File name: model_client.py
import requests
from .schemas import PhiInput

system_prompt = "Translate the following user prompt into Italian."
user_prompt = "Hello my name is Peter."
payload = PhiInput(system_prompt=system_prompt, user_prompt=user_prompt)

response = requests.post("http://127.0.0.1:8000/", json=payload.model_dump())
text = response.text

print(text)
