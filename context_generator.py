import string


class ContextGenerator:
    def __init__(self):
        self.data_path = 'data.csv'
        self.data = self._parse_data()
        self.stopwords_set = self._get_stop_words()

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
                    'doctor': values[0].split(" | "),
                    'patient': values[1].split(" | "),
                    'word_set': word_set,
                })
        return parsed_data

    def _get_stop_words(self):
        stopwords = []
        with open('stopwords.csv', 'r') as f:
            for word in f:
                stopwords.append(word.strip())
        return set(stopwords)

    def _calculate_likelihoods(self, sentence):
        likelihood = []
        sentence_set = set(sentence.lower().split())
        for intent in self.data:
            common_words = sentence_set.intersection(intent['word_set'])
            common_stop_words = sentence_set.intersection(self.stopwords_set)
            # add 1 point for common words. Then, subtract 0.5 likelihood points for each common stop word
            intent['likelihood'] = len(common_words) - (len(common_stop_words) / 2)
            likelihood.append(intent)

        likelihood = sorted(
            likelihood, key=lambda x: x['likelihood'], reverse=True)
        return likelihood

    def generate_context(self, sentence):
        likelihoods = self._calculate_likelihoods(sentence)
        context = "Context: \n"
        for data in likelihoods[:5]:
            context += f"Doctor: {data['doctor'][0]} Tiffany: {data['patient'][0]}\n"
        context += "\nInstructions: Respond to the following question as if you are Tiffany and ensure the response is consistent with the given Context. If you are unsure of the answer, please ask the instructor for clarification.\n\n"
        context += "Q: " + sentence + "\n\nA:"
        print(context)
        return context


if __name__ == "__main__":
    import pprint as pp

    cg = ContextGenerator()
    # cg._calculate_likelihoods("Hello how are you doing today. Is there anything I can do for you?")
    # pp.pprint(cg._calculate_likelihoods("When did this first start happening")[:1])
