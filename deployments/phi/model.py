from typing import Dict
import requests
from starlette.requests import Request

from transformers import AutoModelForCausalLM, AutoProcessor, GenerationConfig
from ray import serve

from .schemas import PhiInput


@serve.deployment(num_replicas=1, ray_actor_options={"num_cpus": 1, "num_gpus": 1})
class Phi4:
    def __init__(self, model_dir) -> None:
        # Load model and processor
        self.processor = AutoProcessor.from_pretrained(
            model_dir, trust_remote_code=True
        )
        self.model = AutoModelForCausalLM.from_pretrained(
            model_dir,
            device_map="cuda",
            torch_dtype="auto",
            trust_remote_code=True,
            _attn_implementation="flash_attention_2",
        ).cuda()

        # Load generation config
        self.generation_config = GenerationConfig.from_pretrained(model_dir)

    def _get_text_prompt(self, system_prompt: str, user_prompt: str) -> str:

        prompt = (
            f"<|system|>{system_prompt}<|end|><|user|>{user_prompt}<|end|><|assistant|>"
        )
        return prompt

    def pipeline(self, model_input: PhiInput) -> str:
        prompt = self._get_text_prompt(
            model_input.system_prompt, model_input.user_prompt
        )

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

    async def __call__(self, http_request: Request) -> str:
        inputs: Dict = await http_request.json()
        model_input = PhiInput(**inputs)
        return self.pipeline(model_input)


phi_app = Phi4.bind(model_dir="microsoft/Phi-4-multimodal-instruct")
# if __name__ == "__main__":

### Local Model Testing
# model_path = "microsoft/Phi-4-multimodal-instruct"
# model = Phi4Translate(model_path)

# system_prompt = "Translate the following user prompt into Chinese Mandarin."
# user_prompt = "Hello my name is Peter"

# model_inputs = PhiInput(system_prompt=system_prompt, user_prompt=user_prompt)

# result = model.pipeline(model_inputs)
# print(result)
