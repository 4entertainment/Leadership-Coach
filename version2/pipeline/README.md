# 📌 README - Pipeline Documentation  

This document provides an overview of the **pipeline workflow** described in the `ReadMeEn-Pipeline.md` file. 🚀

---

## 📌 ingest.py (English)  

This Python script **extracts text embeddings from a JSON file** and saves them to a local directory. The **BAAI/bge-m3** model is used for embedding generation.  

---

### 🛠 **Why This Model?**  
✔ **High retrieval performance** (MTEB leaderboard reference).  
✔ **Supports hybrid search** (handles both dense and sparse vectors).  
✔ **Multilingual capability** for effective cross-language retrieval.  
✔ **Vector database is built using the txtai library.**  

### ⚙ **Usage**  

1. **Install required dependencies:**  
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the script:**  
   ```bash
   python ingest.py
   ```

3. **Where are embeddings stored?**  
   - Embeddings are saved in the **`indexes/`** directory.  
   - Default file name format: **`index_bge-m3_date`**.  
   - Uses **txtai library** for SQLite-based storage.

## 📌 query.py (English)  

This Python script **extracts embeddings from a user query** and performs a **similarity search** over a pre-indexed vector database using `ingest.py`. The **txtai library** is utilized for hybrid search.  

---

### 🛠 **Features**  
✔ **Embeddings for queries are generated using the BGE-M3 model.**  
✔ **Supports hybrid search** (combining dense and sparse vectors).  
✔ **Adjustable hybrid parameter (alpha)** for semantic/syntactic balance.  
✔ **Configurable limit parameter** to control the number of returned documents.  
✔ **Uses txtai vector database** for indexed document retrieval.  
✔ **Interactive query execution** with real-time results.  

### ⚙ **Usage**  

1. **Run the script:**  
   ```bash
   python query.py
   ```

2. **Input Parameters:**  
   - **Hybrid parameter (alpha):** 0.0 - 0.5 favors dense (semantic), 0.5 - 1.0 favors sparse (syntactic).  
   - **Limit parameter:** Defines the number of retrieved documents.  
   
3. **Example Output Format:**  
   ```
   Query: Dijitalleşme mali denetim sektörünü nasıl etkiliyor?
   
   File Title   : Tecrübe Konuşuyor - Hüsnü Güreli
   Transcription: Otomasyon ve yapay zeka kullanımı sayesinde...
   Score        : 0.xyzt
   ------------------------------------------------------------
   ```


## 📌 query_and_llm.py (English)  

This Python script is a Python-based script designed to handle both document retrieval using embeddings and querying a Large Language Model (LLM) for contextual responses. The script builds upon the functionality of `query.py`, with the added feature of integrating a pre-trained LLM (Llama3:70b via Ollama) to generate responses based on the retrieved documents and the user query.

### Key Features:
- **Document Indexing**: Uses `txtai` for indexing and searching documents based on embeddings.
- **Hybrid Search**: Supports hybrid search with customizable weight parameters.
- **LLM Integration**: Queries the Llama3:70b model to generate responses based on the context retrieved from the documents.
- **Contextual Response Generation**: Constructs a comprehensive prompt for the LLM using a Turkish system prompt and the relevant document context.

## Requirements
- Python 3.10.16
- `txtai` for document embedding and retrieval
- Ollama (with Llama3:70b model)
- `subprocess` and `json` libraries (standard in Python)

## How It Works

1. **Embedding Indexing**:
    The `EmbeddingIndexer` class uses `txtai` to create an embedding index from the provided documents (in JSON format). The documents are indexed using the `BGE-M3` model, and the results are stored in a directory. If the index already exists, it will be loaded for future use.

2. **Querying**:
    Users provide a query, and the system uses the embeddings to search for relevant documents. These documents are then combined into a context for the LLM.

3. **LLM Integration**:
    The script sends the retrieved context along with the user query to the Llama3:70b model via the Ollama service. The model is instructed to provide a detailed, accurate response based on the context.

4. **Response**:
    The model generates a response that answers the user’s query based on the provided context. This response is printed to the console.

## Llama3:70b Model Selection

The `llama3:70b` model from Ollama was chosen for this project for its high performance in generating coherent and accurate responses in the Turkish language. It is a robust, large-scale language model with proven capabilities in handling complex queries and diverse domains, making it well-suited for our task of answering queries based on domain-specific documents.

The integration with Ollama simplifies model usage and enhances deployment efficiency, avoiding the complexities of managing local model infrastructure.

## Script Breakdown

### `EmbeddingIndexer` Class

- **`__init__(self, model_name="BAAI/bge-m3", cuda_device="1")`**:
    Initializes the indexing process with the specified model and CUDA settings.
  
- **`load_data(self, json_file)`**:
    Loads documents from a JSON file and prepares them for indexing.
  
- **`prepare_documents(self)`**:
    Prepares documents by combining file titles and transcriptions into a format suitable for indexing.
  
- **`index_documents(self)`**:
    Indexes the prepared documents using `txtai`.
  
- **`save_index(self, directory="indexes")`**:
    Saves the indexed documents to the specified directory.

### `generate_response` Function

- **Generates a response** using the Llama3:70b model by passing the context and query to the model via Ollama. The function constructs a prompt that adheres to the model's system instructions and formats the query and context accordingly.

### Main Workflow

1. Load or index documents.
2. Query the system for relevant documents based on user input.
3. Construct the context from retrieved documents.
4. Generate a response from the LLM using the constructed context.
5. Display the response.

## Usage

1. **Run the script**:

    ```
    python query_and_llm.py
    ```

2. **Follow the prompts**:
    - Enter your search query when prompted.
    - Specify the limit and weight parameters for the hybrid search.

3. **Review the Results**:
    - The script will display the top matching documents.
    - It will then display the LLM-generated response based on the query and context.
