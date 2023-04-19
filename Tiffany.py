from context_generator import ContextGenerator
from alpaca import Alpaca
import sys


class Tiffany:
    def __init__(self):
        self.context_generator = ContextGenerator()
        self.alpaca = Alpaca()

    def _txt_file_to_string(self, path):
        with open(path, 'r') as f:
            return f.read()

    def __call__(self, sentence):
        prompt = self.context_generator.generate_context(sentence)
        return self.alpaca.evaluate(prompt)

    def chat(self, sentence):
        self(sentence)

    def start_chat(self):
        exit_code = False
        while not exit_code:
            sentence = input(f"Ask Tiffany: ")
            if sentence == "exit":
                exit_code = True
                sys.exit()
            else:
                print(f"Tiffany: ", self(sentence))


if __name__ == "__main__":
    tiffany = Tiffany()
    tiffany.start_chat()
