from peft import PeftModel
from transformers import LLaMATokenizer, LLaMAForCausalLM, GenerationConfig


class Alpaca:
    def __init__(self):
        self.tokenizer = LLaMATokenizer.from_pretrained(
            "decapoda-research/llama-7b-hf")
        self.model = PeftModel.from_pretrained(LLaMAForCausalLM.from_pretrained(
            "decapoda-research/llama-7b-hf",
            load_in_8bit=True,
            device_map={"": 'cpu'},
        ), "tloen/alpaca-lora-7b")
        self.generation_config = GenerationConfig(
            temperature=0.1,
            top_p=0.75,
            num_beams=4,)

    def evaluate(self, instruction):
        prompt = self.generate_prompt(instruction)
        inputs = self.tokenizer(prompt, return_tensors="pt")
        input_ids = inputs["input_ids"].cuda()
        generation_output = self.model.generate(
            input_ids=input_ids,
            generation_config=self.generation_config,
            return_dict_in_generate=True,
            output_scores=True,
            max_new_tokens=4097
        )
        for s in generation_output.sequences:
            output = self.tokenizer.decode(s)
            print("Response:", output.split("### A:")[1].strip())
