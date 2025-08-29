import requests
import torch
import os
import io
from PIL import Image
import soundfile as sf
from transformers import AutoModelForCausalLM, AutoProcessor, GenerationConfig
from urllib.request import urlopen

import requests
from starlette.requests import Request
from typing import Dict

from ray import serve


class Phi4Translate:
    def __init__(self, model_dir) -> None:
        # Load model and processor
        self.processor = AutoProcessor.from_pretrained(
            model_path, trust_remote_code=True
        )
        self.model = AutoModelForCausalLM.from_pretrained(
            model_dir,
            device_map="cuda",
            torch_dtype="auto",
            trust_remote_code=True,
            _attn_implementation="flash_attention_2",
        ).cuda()

        # Load generation config
        self.generation_config = GenerationConfig.from_pretrained(model_path)

    def _get_text_prompt(self, system_prompt: str, user_prompt: str) -> str:

        prompt = (
            f"<|system|>{system_prompt}<|end|><|user|>{user_prompt}<|end|><|assistant|>"
        )
        return prompt

    def pipeline(self, system_prompt: str, user_prompt: str) -> str:
        prompt = self._get_text_prompt(user_prompt, system_prompt)

        # Pre-process
        inputs = self.processor(text=prompt, return_tensors="pt").to("cuda:0")

        # Inference
        generate_ids = self.model.generate(
            **inputs,
            max_new_tokens=1000,
            generation_config=self.generation_config,
        )

        # Post-process
        generate_ids = generate_ids[:, inputs["input_ids"].shape[1] :]
        response = self.processor.batch_decode(
            generate_ids, skip_special_tokens=True, clean_up_tokenization_spaces=False
        )[0]
        return response


if __name__ == "__main__":

    model_path = "microsoft/Phi-4-multimodal-instruct"
    model = Phi4Translate(model_path)

    system_prompt = "Translate the following user prompt into French."
    user_prompt = "Hello my name is Peter"

    model.pipeline()
