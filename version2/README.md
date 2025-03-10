# Leadership Coach Streamlit Application

This Streamlit application is designed to provide users with leadership coaching through the use of natural language processing (NLP) models, document indexing, and a text-to-speech (TTS) system. It allows users to search for relevant documents, generate responses from a large language model (LLM), and interact with the application via a virtual assistant that speaks the responses.

## Features

- **Search**: Users can search for documents using a query, with options to set a limit for results and weight for hybrid search.
- **Hybrid Search**: Leverages embeddings and a hybrid approach for better search results.
- **Text-to-Speech (TTS)**: Converts LLM responses into speech using the Facebook MMS TTS model (`facebook/mms-tts-tur`).
- **Web Search**: Allows users to search the web using DuckDuckGo (although it may not be working due to connection issues).
- **CUDA Support**: The application supports GPU acceleration using CUDA for faster processing.

## Technologies Used

- **Streamlit**: For building the user interface.
- **txtai**: For document indexing and searching using embeddings.
- **Ollama**: For running Llama3-based large language model (LLM).
- **Facebook MMS TTS**: For converting text responses into speech.
- **DuckDuckGo Search API**: For web search functionality.
- **PyTorch**: For running deep learning models.
- **Scipy**: For handling WAV file output for TTS.

## Installation

### Prerequisites

- Python 3.8+
- CUDA-enabled GPU (optional but recommended for better performance)
- The following Python packages:
  - `streamlit`
  - `txtai`
  - `torch`
  - `scipy`
  - `transformers`
  - `duckduckgo_search`

### Steps

1. Clone the repository:
   ```bash
   git clone <your-repository-url>
   cd <your-repository-folder>
Create a virtual environment (optional but recommended):

bash
Copy
Edit
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
Install the required dependencies:

pip install -r requirements.txt
Ensure you have the necessary models downloaded:

facebook/mms-tts-tur for TTS functionality.
Llama3 model via ollama for generating responses.
Run the application:

streamlit run app.py
This will launch the Streamlit application in your browser at http://localhost:8081.

Usage
Search Query: Enter a search query to retrieve relevant documents.
Search Parameters:
Limit: Set a limit for the number of results (default: 3).
Hybrid Search Weight: Set a weight for hybrid search (optional).
View Results: Once the query is submitted, the relevant documents will be displayed.
LLM Response: The system generates a response based on the search context and user query, which is then spoken using the TTS model.
Web Search: (Experimental) You can also search the web for additional information using DuckDuckGo, although the feature may face connectivity issues at times.
Known Issues
DuckDuckGo Search: The web search feature (search_web_results_duckduckgo) may not work as expected due to network issues. Ensure that the app has an active internet connection or try again later.
