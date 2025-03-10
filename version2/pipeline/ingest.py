import json
import os
import time
from datetime import datetime
from txtai import Embeddings
from tqdm import tqdm


class EmbeddingIndexer:
    def __init__(self, model_name="BAAI/bge-m3", cuda_device="1"):
        """
        Initialize the embedding indexer with the given model and CUDA settings.
        """
        os.environ["CUDA_VISIBLE_DEVICES"] = cuda_device
        self.model_name = model_name
        # Create a txtai Embeddings instance with desired settings.
        self.embeddings = Embeddings(path=model_name, hybrid=True, content=True, method="clspooling")
        self.data = {}
        self.documents = []

    def load_data(self, json_file):
        """
        Load data from a JSON file.
        :param json_file: Path to the JSON file.
        """
        with open(json_file, "r", encoding="utf-8") as f:
            self.data = json.load(f)
        return self.data

    def prepare_documents(self):
        """
        Prepare documents by combining file title and transcription.
        Each document is a tuple: (id, combined_text, metadata)
        The metadata is JSON serialized to ensure SQLite can bind it properly.
        """
        self.documents = []
        for key, value in self.data.items():
            file_title = value.get("file_title", "")
            transcription = value.get("transcription", "")
            # Combine file title and transcription in a structured way.
            combined_text = f"File Title: {file_title}\nTranscription: {transcription}"
            # Serialize metadata as JSON to avoid binding errors in SQLite.
            metadata = json.dumps({"file_title": file_title, "transcription": transcription})
            # Append the document as a tuple.
            self.documents.append((key, combined_text, metadata))
        return self.documents

    def index_documents(self):
        """
        Index all prepared documents using txtai.
        """
        if not self.documents:
            raise ValueError("No documents prepared for indexing. Run prepare_documents() first.")
        print("Indexing documents...")
        start_time = time.time()
        # Index the documents with a progress bar.
        self.embeddings.index(tqdm(self.documents, total=len(self.documents)))
        elapsed_time = time.time() - start_time
        print(f"Indexing took {elapsed_time:.2f} seconds")
        return elapsed_time

    def save_index(self, directory="indexes"):
        """
        Save the index to the specified directory.
        :param directory: Directory where the index file will be saved.
        """
        if not os.path.exists(directory):
            os.makedirs(directory)
        current_date = datetime.now().strftime("%d-%m-%Y")
        file_name = f"index_{self.model_name.split('/')[-1]}_{current_date}"
        file_path = os.path.join(directory, file_name)
        self.embeddings.save(file_path)
        print("Index saved to", file_path)
        return file_path


if __name__ == "__main__":
    # Example usage:
    indexer = EmbeddingIndexer(model_name="BAAI/bge-m3", cuda_device="1")
    indexer.load_data("transcriptions-no-cut.json")
    indexer.prepare_documents()
    indexer.index_documents()
    indexer.save_index()
