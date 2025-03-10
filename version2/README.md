# Leadership Coach Project 🚀

This project is designed to provide users with leadership coaching through the use of natural language processing (NLP) models, document indexing, and a text-to-speech (TTS) system. It allows users to search for relevant documents, generate responses from a large language model (LLM), and interact with the application via a virtual assistant that speaks the responses.

## Features

- **Search**: Users can search for documents using a query, with options to set a limit for results and weight for hybrid search.
- **Hybrid Search**: Leverages embeddings and a hybrid approach for better search results.
- **Text-to-Speech (TTS)**: Converts LLM responses into speech using the Facebook MMS TTS model (`facebook/mms-tts-tur`).
- **Speech-to-Text (STT)**: Converts user speech into text to interact with the application via voice.
- **Web Search**: Allows users to search the web using DuckDuckGo (although it may not be working due to connection issues).
- **CUDA Support**: The application supports GPU acceleration using CUDA for faster processing.
- **YouTube Playlist Download**: Users can download MP3 and MP4 files from YouTube playlists and convert them to text format.
- **RAG Architecture**: After a search, the resulting text is used to feed into an LLM, implementing a Retrieval-Augmented Generation (RAG) architecture for domain-based, field-based information retrieval. This enables better extraction of domain-specific knowledge.

## Technologies Used

- **Streamlit**: For building the user interface.
- **txtai**: For document indexing and searching using embeddings.
- **Ollama**: For running Llama3-based large language model (LLM).
- **Facebook MMS TTS**: For converting text responses into speech.
- **DuckDuckGo Search API**: For web search functionality.
- **PyTorch**: For running deep learning models.
- **Scipy**: For handling WAV file output for TTS.
- **YouTube API**: For downloading MP3 and MP4 files from YouTube playlists.
- **Speech Recognition**: For converting speech to text.

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
  - `youtube-dl` or `yt-dlp`
  - `SpeechRecognition`


### Steps

1. Clone the repository:
    ```bash
    git clone https://github.com/4entertainment/Leadership-Coach.git
    cd Leadership-Coach/version2
    ```

2. Create a conda environment (optional but recommended):

    ```bash
    python create --name my_env python==3.10.16
    conda activate my_env
    ```

3. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```
    Ensure you have the necessary models downloaded:

    - `openai/whisper-large-v3` for audio-to-text processing
    - `bge-m3` for text-embedding extraction
    - `facebook/mms-tts-tur` for TTS functionality.
    - `Llama3:70b` model via ollama for generating responses.

4. Get your API-Key:

    It is not necessary but if you want to use ElevenLabs speech-to-text script at the project; please go to `.env` file, change your ElevenLabs API KEY in this part of code: 
    ```bash
    ELEVENLABS_API_KEY=MY_API_KEY
    ```

5. Run the application:

    ```bash
    streamlit run app.py
    ```
    This will launch the Streamlit application in your browser at http://localhost:8081.

## Usage
- **Search Query:** Enter a search query to retrieve relevant documents.
- **Search Parameters:**
    - *Limit:* Set a limit for the number of results (default: 3).
    - *Hybrid Search Weight:* Set a weight for hybrid search (optional).
- **View Results:** Once the query is submitted, the relevant documents will be displayed.
- **LLM Response:** The system generates a response based on the search context and user query, which is then spoken using the TTS model.
- **LLM Response as Text-to-Speech:** The system generates a response based on the search context and user query. This response is then converted to speech using the TTS model and delivered to the user, acting like a virtual assistant.
- **Web Search**: (Experimental) Users can search the web using DuckDuckGo for additional information. However, this feature may not function properly due to connectivity issues. The functionality might be affected by internet connection problems or issues with the DuckDuckGo API, meaning the web search may not work as expected. Therefore, this feature is currently limited or non-functional.



## Known Issues and Future Improvements
- **Web Search:** The functionality may be affected by internet connection problems or issues with the DuckDuckGo API, meaning the web search may not work as expected. Therefore, this feature is currently limited or non-functional. Alternative solutions such as using libraries like BeautifulSoup, Requests, or Serapi (with an API key) for web searching could have been explored, but due to time constraints, they were not implemented.

- **Web Search:** Regarding the web search functionality, although it was added in a non-functional state, it was designed to be user-dependent. In other words, the use case was intended to perform a web search based on a query provided by the user. However, a further improvement idea emerged: when the LLM generates responses like "Bilmiyorum." or "Bilgim yok." an automatic web search could have been triggered to provide a more insightful answer. This would have resulted in an AI-based solution, and if necessary, the web search results could have been presented to the user separately. Allowing the LLM to make this decision would have been an innovative approach.

- **Text-to-Speech Processing:** For speech-to-text processing, the "openai/whisper-large-v3" model was used. However, it was later discovered that ElevenLabs' API provides a much more efficient solution for speech-to-text tasks. Due to time limitations and the exhaustion of the API key quota, integrating ElevenLabs into the project was not feasible.

- **Web Hosting and Accessibility:** At the final stage, a hosting request was made to enable "Web Accessibility: Making the Coach accessible through a web link." However, this could not be achieved for the following reasons:

    - The development environment used for the project, including the video capture environment, was only available for a limited period. The project development time was constrained to just 3.5 days, which was insufficient for setting up a hosting solution.

    - Additionally, serving the project was not feasible because multiple large models were used to achieve performance. These models include:

        - Llama 3:70b
        - BGE-M3
        - Whisper

    Since a number of large models were utilized to achieve the necessary performance, setting up serving in a production environment was not practical. Furthermore, the development environment was provided under specific terms, and serving was not permitted within that environment. **As the developer, I take responsibility for this limitation.** However, with more time, I had planned to rent a GPU from platforms like Vast.ai (https://vast.ai/) or Google Colab (https://colab.research.google.com/) and perform the serving using Streamlit Deployment (Relative links: https://docs.streamlit.io/deploy/tutorials and https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app) to enable web accessibility.
