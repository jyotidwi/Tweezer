import pickle
import re
from pathlib import Path

import numpy as np
from gensim.models import Word2Vec
from nltk.tokenize import word_tokenize
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tqdm import tqdm


class Model():

    def __init__(self, model_path="TweezerMDL"):
        self.model_path = model_path
        self._list_of_vector_information = []

    def _get_code_from_decom_file(self, path_to_file):

        with open(path_to_file, "r") as file:
            code = file.read()
            # Define a regular expression pattern to match the function body
            pattern = re.compile(r'\{([^}]*)\}', re.DOTALL)

            # Find the first match in the code
            match = pattern.search(code)

            if match:
                # Extract and return the function body
                return match.group(1).strip()

            return None

    def function_to_vec(self, code, max_length=100):
        # Preprocess the code: remove non-alphanumeric characters and split into words
        clean_code = re.sub(r'[^a-zA-Z0-9 ]', '', code)
        tokenized_code = word_tokenize(clean_code.lower())

        # Define and train the Word2Vec model
        model = Word2Vec([tokenized_code], vector_size=100, window=5, min_count=1, workers=4)

        # Convert the code snippet to vectors
        vectorized_code = [model.wv[word] for word in tokenized_code if word in model.wv]

        # Pad or truncate the vectors to the specified maximum length
        vectorized_code = \
        pad_sequences([vectorized_code], maxlen=max_length, dtype='float32', padding='post', truncating='post')[0]

        return vectorized_code

    def _function_file_to_vec(self, path):
        code = self._get_code_from_decom_file(path)
        return self.function_to_vec(code)

    def save_model(self):
        with open(self.model_path, 'wb') as file:
            pickle.dump(self._list_of_vector_information, file)

    def read_model(self):
        with open(self.model_path, 'rb') as file:
            return pickle.load(file)

    def get_vectors_from_files(self, decom_files_dir):

        if Path(self.model_path).is_file():
            self._list_of_vector_information = self.read_model()

        for file_path in tqdm(Path(decom_files_dir).iterdir(),
                              desc="Getting vectors from files in {}".format(decom_files_dir)):

            binary_name, function_name, *epoc = Path(file_path).name.split("__")

            # No value in vectorising functions that don't have names
            if str(function_name).startswith("FUN") or str(function_name).startswith("thunk"):
                continue

            combo_exists = any(
                item["function_name"] == function_name and item["binary"] == binary_name for item in
                self._list_of_vector_information)

            if not combo_exists:
                self._list_of_vector_information.append(
                    {"function_name": function_name, "vector": self._function_file_to_vec(file_path),
                     "binary": binary_name})

        self.save_model()

    def find_similar_vectors(self, vector_to_compare, number_of_closest=10):
        # Convert the list of vectors to a 2D NumPy array
        vector_list = [item['vector'] for item in self._list_of_vector_information]

        if len(vector_list) <= 0:
            raise Exception("Model contains 0 vectors - extend model!")

        vectors_array = np.array(vector_list)

        # Ensure new_vector is a 1D array or has a compatible shape
        new_vector = np.squeeze(vector_to_compare)

        # Compute the cosine similarity between the new vector and all vectors in the list
        similarities = np.dot(vectors_array, new_vector) / (
                np.linalg.norm(vectors_array, axis=1) * np.linalg.norm(new_vector))

        # Combine similarities with function names
        function_similarities = zip([item['function_name'] for item in self._list_of_vector_information], similarities)

        # Sort by similarity and get the top 10
        sorted_function_similarities = sorted(function_similarities, key=lambda x: x[1], reverse=True)[
                                       :number_of_closest]

        # Extract function names
        closest_function_names = [item[0] for item in sorted_function_similarities]

        return closest_function_names


if __name__ == '__main__':
    raise Exception("This is not an entrypoint!")
