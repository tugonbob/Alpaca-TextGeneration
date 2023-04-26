import pickle
from sentence_transformers import SentenceTransformer
import numpy as np
import openai
import time


class MLContextGenerator:
    def __init__(self, data_path, nearest=100):
        self.data_path = data_path
        self.nearest = nearest
        self.df = pickle.load(open(self.data_path, "rb"))
        self.model = "gpt-3.5-turbo"

    def _get_embedding(self, sentence):
        model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
        embedding = model.encode(sentence)
        return embedding

    def _sentence_search(self, sentence):
        # get embedding for sentence
        embedding = self._get_embedding(sentence)
        # get nearest neighbors
        nearest_neighbors = self.df["embeddings"].apply(
            lambda x: self._cosine_similarity(x, embedding)
        )
        # sort nearest neighbors
        nearest_neighbors = nearest_neighbors.sort_values(ascending=False)
        # get top nearest neighbors
        nearest_neighbors = nearest_neighbors.iloc[: self.nearest]
        # get index of nearest neighbors
        nearest_neighbors_index = nearest_neighbors.index
        # get sentences from nearest neighbors
        nearest_neighbors_sentences = self.df.iloc[nearest_neighbors_index, 0]
        # convert to list
        nearest_neighbors_list = nearest_neighbors_sentences.tolist()
        # loop through nearest neighbors and remove tags
        for i in range(len(nearest_neighbors_list)):
            text = nearest_neighbors_list[i]
            nearest_neighbors_list[i] = text
        return self._list_2_str(nearest_neighbors_list)

    def _cosine_similarity(self, x, y):
        return np.dot(x, y) / (np.linalg.norm(x) * np.linalg.norm(y))

    def _list_2_str(self, list):
        return " ".join(list)

    def generate_context(self, sentence):
        print("sentence searching")
        search = self._sentence_search(sentence)
        print("summarizing")
        summary = self.summarize(search)
        return summary

    def summarize(self, sentence):
        start = time.time()
        task = "summarize the following memory in second person past tense"
        system_context = f"You are a helpful assistant that will {task}. Start the resonse with I remember"

        openai.api_key = "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"
        response = openai.ChatCompletion.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_context},
                {"role": "user", "content": sentence},
            ],
        )

        gpt_response = response["choices"][0]["message"]["content"]
        end = time.time()

        print(f"Time to generate dynamic context: {end - start}")

        return gpt_response
