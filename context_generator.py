import string


class ContextGenerator:
    def __init__(self):
        self.data_path = '/Users/joshuagao/SVS/Alpaca-TextGeneration/data.csv'
        self.data = self._parse_data()

    def _parse_data(self):
        parsed_data = []
        with open(self.data_path, 'r') as data:
            for line in data:
                # split questions and answers
                values = line.strip().split('\t')
                # combine question and answer string, and remove punctuation
                no_punctuation = (
                    values[0] + values[1]).translate(str.maketrans("", "", string.punctuation))
                # lowercase combined Q and A
                lowercased = no_punctuation.lower()
                word_set = set(lowercased.split())
                parsed_data.append({
                    'doctor': values[0],
                    'patient': values[1],
                    'word_set': word_set,
                })
        return parsed_data

    def _calculate_likelihoods(self, sentence):
        likelihood = []
        sentence_set = set(sentence.lower().split())
        for intent in self.data:
            common_words = sentence_set.intersection(intent['word_set'])
            intent['likelihood'] = len(common_words)
            likelihood.append(intent)
        likelihood = sorted(
            likelihood, key=lambda x: x['likelihood'], reverse=True)
        return likelihood

    def generate_context(self, sentence):
        likelihoods = self._calculate_likelihoods(sentence)

        context = ""
        for data in likelihoods[:16]:
            context += f"Doctor: {data['doctor']} Tiffany: {data['patient']}\n"
        context += "\nQ: Respond to the following questions as if you are Tiffany and ensure the response is consistent with the given Context. If you are unsure of the answer, please ask the instructor for clarification. "
        context += sentence + "\n\nA:"
        print(context)
        return context


if __name__ == "__main__":
    import pprint as pp

    cg = ContextGenerator()
    context = cg.generate_context("Hi")
    print(context)
