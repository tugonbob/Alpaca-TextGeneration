import sys
from peft import PeftModel
from transformers import LLaMATokenizer, LLaMAForCausalLM, GenerationConfig

tokenizer = LLaMATokenizer.from_pretrained("decapoda-research/llama-7b-hf")
model = LLaMAForCausalLM.from_pretrained(
    "decapoda-research/llama-7b-hf",
    load_in_8bit=True,
    device_map={"": 'cpu'},
)
model = PeftModel.from_pretrained(model, "tloen/alpaca-lora-7b")

def generate_prompt(instruction):
  return f"""
### Context:
Respond to the following questions as if you are Tiffany and ensure the response is consistent with the given Context. If you are unsure of the answer, please ask the instructor for clarification. Context: Tiffany is a patient who doesn't know she is dehydrated. She is a middle aged woman and likes to go running. She normaly runs in the morning, but she ran in the afternoon today because she didn't have time. It was much hotter in the afternoon and she became dehydrated with all its associated symptoms

### Q:
{instruction}

### A:"""

generation_config = GenerationConfig(
    temperature=0.1,
    top_p=0.75,
    num_beams=4,
)

def evaluate(instruction):
    prompt = generate_prompt(instruction)
    inputs = tokenizer(prompt, return_tensors="pt")
    input_ids = inputs["input_ids"].cuda()
    generation_output = model.generate(
        input_ids=input_ids,
        generation_config=generation_config,
        return_dict_in_generate=True,
        output_scores=True,
        max_new_tokens=256
    )
    for s in generation_output.sequences:
        output = tokenizer.decode(s)
        print("Response:", output.split("### A:")[1].strip())

while(True):
  sentence = input("Ask Tiffany: ")
  if sentence == 'Exit':
    sys.exit()
  evaluate(sentence)