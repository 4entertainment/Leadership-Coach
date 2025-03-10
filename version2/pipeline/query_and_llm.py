import json
import os
import time
import subprocess
from datetime import datetime
from txtai import Embeddings
from tqdm import tqdm

#########################
# txtai Indexing Module #
#########################

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
            combined_text = f"Dosya Başlığı: {file_title}\nTranskript: {transcription}"
            metadata = json.dumps({"file_title": file_title, "transcription": transcription})
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

#############################
# LLM Generation Components #
#############################

def generate_response(context, query_text):
    """
    Generate a response using the llama3-70b model via Ollama with a Turkish system prompt.
    The prompt instructs the model to use the provided context to produce a comprehensive, accurate, and clear answer.
    """
    prompt = f"""Sistem Talimatları:
Alanında uzman, detaylara önem veren ve doğruluğa bağlı kalan bir dil modelisin. Aşağıda verilen bağlamı kullanarak, '{query_text}' sorusuna kapsamlı, doğru ve net bir yanıt oluştur. Lütfen verilen bağlamdaki bilgileri dikkatle değerlendir ve gereksiz tahminlerden kaçın. Eğer sağlanan metinlerde gerekli bilgi yoksa, "Bilmiyorum" de.

--- BAĞLAM ---
{context}

--- SORU ---
{query_text}

--- YANIT ---"""
    try:
        # Pass the prompt as a positional argument instead of using the --prompt flag.
        result = subprocess.run(
            ["ollama", "run", "llama3:70b", prompt],
            capture_output=True, text=True, check=True
        )
        response = result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print("Ollama error:", e.stderr)
        response = "An error occurred while generating a response with Ollama."
    return response

###############################
# Main Query and Integration  #
###############################

def main():
    # Set the index directory path
    index_dir = "/data/Workspace/balkan/leadership_coach/indexes"
    indexer = EmbeddingIndexer(model_name="BAAI/bge-m3", cuda_device="1")
    current_date = datetime.now().strftime("%d-%m-%Y")
    index_file_name = f"index_{indexer.model_name.split('/')[-1]}_{current_date}"
    index_file_path = os.path.join(index_dir, index_file_name)

    # If the index file exists, load it; otherwise, index the documents and save the index.
    if os.path.exists(index_file_path):
        print("Loading existing index from", index_file_path)
        indexer.embeddings.load(index_file_path)
        # Even if the index is loaded, we need the documents for mapping context.
        indexer.load_data("transcriptions-no-cut.json")
        indexer.prepare_documents()
    else:
        print("Index file not found. Indexing documents...")
        indexer.load_data("transcriptions-no-cut.json")
        indexer.prepare_documents()
        indexer.index_documents()
        indexer.save_index(directory=index_dir)

    # Ask the user for a query.
    query_text = input("Enter your search query: ").strip()

    # Ask the user for limit and a single weight value for hybrid search.
    limit_input = input("Enter limit parameter for search (default 3): ").strip()
    limit = int(limit_input) if limit_input else 3

    weight_input = input("Enter weight parameter for hybrid search (single value, e.g., 0.5) (default None): ").strip()
    if weight_input:
        weight = float(weight_input)
    else:
        weight = None

    # Retrieve the top results.
    results = indexer.embeddings.search(query_text, limit=limit, weights=weight)
    if not results:
        print("No relevant documents found.")
        return

    # Build context by mapping document IDs to their data.
    doc_dict = {doc[0]: doc for doc in indexer.documents}
    context_pieces = []
    print("\n### Retrieved Documents ###\n")
    for res in results:
        # If result is a dictionary, use the 'id' key; otherwise, assume tuple structure.
        if isinstance(res, dict):
            doc_id = res.get("id")
        else:
            doc_id = res[0]
        if doc_id in doc_dict:
            metadata = json.loads(doc_dict[doc_id][2])
            file_title = metadata.get("file_title", "N/A")
            transcription = metadata.get("transcription", "N/A")
            # Print each retrieved document (in Turkish)
            print(f"Başlık: {file_title}")
            print(f"Transkript: {transcription}")
            print("-" * 50)
            context_pieces.append(f"Başlık: {file_title}\nTranskript: {transcription}")
        else:
            print("Document information not found.")
            context_pieces.append("Document information not found.")
    context = "\n\n".join(context_pieces)

    # Generate the LLM response using the assembled context.
    final_response = generate_response(context, query_text)
    print("\n### LLM Response ###\n")
    print(final_response)

if __name__ == '__main__':
    main()
