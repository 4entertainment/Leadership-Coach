import json
import os
import time
import subprocess
import io
import numpy as np
from datetime import datetime

import streamlit as st
import torch
import scipy.io.wavfile
from txtai import Embeddings
from tqdm import tqdm
from transformers import VitsModel, AutoTokenizer
from duckduckgo_search import DDGS

# Sayfa konfigürasyonu (geniş ekran, sayfa başlığı vs.)
st.set_page_config(layout="wide", page_title="🎖️ Leadership Coach", initial_sidebar_state="expanded")
st.title("🎖️ Leadership Coach")

##############################################
# txtai Indexing ve LLM Yanıt Fonksiyonları  #
##############################################

class EmbeddingIndexer:
    def __init__(self, model_name="BAAI/bge-m3", cuda_device="1"):
        """
        Belirtilen model ve CUDA ayarları ile embedding indexer'ı başlatır.
        """
        os.environ["CUDA_VISIBLE_DEVICES"] = cuda_device
        self.model_name = model_name
        # txtai Embeddings örneğini oluşturuyoruz.
        self.embeddings = Embeddings(path=model_name, hybrid=True, content=True, method="clspooling")
        self.data = {}
        self.documents = []

    def load_data(self, json_file):
        """
        JSON dosyasından veriyi yükler.
        """
        with open(json_file, "r", encoding="utf-8") as f:
            self.data = json.load(f)
        return self.data

    def prepare_documents(self):
        """
        Dokümanları, dosya başlığı ve transkripti birleştirerek hazırlar.
        Her doküman: (id, birleşik metin, metadata) şeklinde.
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
        Hazırlanan dokümanları txtai ile indeksler.
        """
        if not self.documents:
            raise ValueError("İndeksleme için doküman bulunamadı. Önce prepare_documents() çalıştırın.")
        st.info("Dokümanlar indeksleniyor...")
        start_time = time.time()
        self.embeddings.index(tqdm(self.documents, total=len(self.documents)))
        elapsed_time = time.time() - start_time
        st.success(f"İndeksleme {elapsed_time:.2f} saniyede tamamlandı.")
        return elapsed_time

    def save_index(self, directory="indexes"):
        """
        İndeksi belirtilen dizine kaydeder.
        """
        if not os.path.exists(directory):
            os.makedirs(directory)
        current_date = datetime.now().strftime("%d-%m-%Y")
        file_name = f"index_{self.model_name.split('/')[-1]}_{current_date}"
        file_path = os.path.join(directory, file_name)
        self.embeddings.save(file_path)
        st.info("İndeks kaydedildi: " + file_path)
        return file_path

# Web Search Function (No API Key)
def search_web_results_duckduckgo(query, max_results=5):
    """
    DuckDuckGo kullanarak API anahtarsız web araması yapar.
    """
    try:
        ddgs = DDGS()
        results = list(ddgs.text(query, max_results=max_results))
        return results
    except Exception as e:
        st.error(f"Web araması sırasında hata oluştu: {str(e)}")
        return []

def generate_response(context, query_text):
    """
    Ollama aracılığıyla llama3-70b modelini çalıştırır ve LLM yanıtını üretir.
    """
    prompt = f"""Sistem Talimatları:
    Sen yalnızca Türkçe yanıt veren bir yapay zeka asistanısın.
    Başka bir dilde yanıt vermemelisin.

    Aşağıdaki bağlamı kullanarak, '{query_text}' sorusuna yalnızca Türkçe olarak yanıt oluştur.
    Bağlamda verilen bilgilerden emin olmadığın durumda yanıt üretme.
    Gereksiz yorum veya tahmin yapma.
    Eğer bağlamda yeterli bilgi yoksa, sadece "Bilmiyorum." diye yanıt ver.

    --- BAĞLAM ---
    {context}

    --- SORU ---
    {query_text}

    --- YANIT ---"""
    try:
        result = subprocess.run(
            ["ollama", "run", "llama3:70b", prompt],
            capture_output=True, text=True, check=True
        )
        response = result.stdout.strip()
    except subprocess.CalledProcessError as e:
        st.error("Ollama hatası: " + e.stderr)
        response = "Ollama ile yanıt üretilirken bir hata oluştu."
    return response

# LLM yanıtlarını cache'lemek için yeni fonksiyon
@st.cache_data(show_spinner=False)
def cached_generate_response(context, query_text):
    return generate_response(context, query_text)

#########################################
# TTS Model Yükleme ve Ses Üretim Fonksiyonu #
#########################################

@st.cache_resource
def load_tts_model_and_tokenizer():
    model = VitsModel.from_pretrained("facebook/mms-tts-tur")
    tokenizer = AutoTokenizer.from_pretrained("facebook/mms-tts-tur")
    return model, tokenizer

tts_model, tts_tokenizer = load_tts_model_and_tokenizer()

#########################################
# Embedding Indexer'ı Yükleme veya Oluşturma #
#########################################

@st.cache_resource
def load_indexer():
    index_dir = "/data/Workspace/balkan/leadership_coach/indexes"
    indexer = EmbeddingIndexer(model_name="BAAI/bge-m3", cuda_device="1")
    current_date = datetime.now().strftime("%d-%m-%Y")
    index_file_name = f"index_{indexer.model_name.split('/')[-1]}_{current_date}"
    index_file_path = os.path.join(index_dir, index_file_name)

    if os.path.exists(index_file_path):
        st.info("Önceden oluşturulmuş indeks yükleniyor: /indexes/index_bge-m3_10-03-2025")# + # index_file_path)
        indexer.embeddings.load(index_file_path)
        indexer.load_data("transcriptions-no-cut.json")
        indexer.prepare_documents()
    else:
        st.info("İndeks dosyası bulunamadı. Dokümanlar indeksleniyor...")
        indexer.load_data("transcriptions-no-cut.json")
        indexer.prepare_documents()
        indexer.index_documents()
        indexer.save_index(directory=index_dir)
    return indexer

indexer = load_indexer()

#########################################
# Kullanıcı Arayüzü - Sorgu ve İşlemler #
#########################################

st.subheader("Arama Sorgusu Girin")
query_text = st.text_input("Arama sorgunuzu giriniz:")

with st.form("query_params"):
    limit_input = st.text_input("Arama limiti (Varsayılan: 3):", "3")
    weight_input = st.text_input("Hybrid search için ağırlık (Örnek: 0.5, Varsayılan: None):", "")
    submitted = st.form_submit_button("Ara")
    
if submitted and query_text:
    # Parametreleri al
    try:
        limit = int(limit_input)
    except ValueError:
        limit = 3
    try:
        weight = float(weight_input) if weight_input.strip() != "" else None
    except ValueError:
        weight = None

    # Arama işlemi
    results = indexer.embeddings.search(query_text, limit=limit, weights=weight)
    if not results:
        st.warning("İlgili doküman bulunamadı.")
    else:
        # Doküman bilgilerini topla ve ekrana yazdır
        doc_dict = {doc[0]: doc for doc in indexer.documents}
        context_pieces = []
        st.subheader("Elde Edilen Dokümanlar")
        for res in results:
            if isinstance(res, dict):
                doc_id = res.get("id")
            else:
                doc_id = res[0]
            if doc_id in doc_dict:
                metadata = json.loads(doc_dict[doc_id][2])
                file_title = metadata.get("file_title", "N/A")
                transcription = metadata.get("transcription", "N/A")
                st.markdown(f"**Başlık:** {file_title}")
                st.markdown(f"**Transkript:** {transcription}")
                st.markdown("---")
                context_pieces.append(f"Başlık: {file_title}\nTranskript: {transcription}")
            else:
                st.error("Doküman bilgisi bulunamadı.")
                context_pieces.append("Doküman bilgisi bulunamadı.")
        context = "\n\n".join(context_pieces)

        # LLM yanıtını üret (cache'lenmiş fonksiyon kullanılıyor)
        st.subheader("LLM Yanıtı")
        final_response = cached_generate_response(context, query_text)
        st.write(final_response)

        #########################################
        # TTS: Yanıtı Sese Dönüştürme          #
        #########################################
        st.subheader("Sesli Yanıt")
        with st.spinner("Ses oluşturuluyor..."):
            inputs = tts_tokenizer(final_response, return_tensors="pt")
            with torch.no_grad():
                result = tts_model(**inputs)
                waveform = result.waveform.detach().cpu().numpy()

            if waveform.ndim > 1:
                waveform = waveform.squeeze()
            waveform_norm = waveform / np.max(np.abs(waveform))
            waveform_int16 = (waveform_norm * 32767).astype(np.int16)
            sampling_rate = tts_model.config.sampling_rate

            wav_buffer = io.BytesIO()
            scipy.io.wavfile.write(wav_buffer, rate=sampling_rate, data=waveform_int16)
            wav_buffer.seek(0)
            st.audio(wav_buffer, format="audio/wav")
            st.success("Ses oluşturuldu!")
            
            st.subheader("Web Search Yapılsın mı?")
            if st.checkbox("Web Search Yapılsın mı?"):
                search_results = search_web_results_duckduckgo(query_text, max_results=5)
                for result in search_results:
                    st.markdown(f"**[{result.get('title', 'Başlık Yok')}]({result.get('href', '#')})**")
                    st.write(result.get("body", "Açıklama Yok"))
                    st.markdown("---")
