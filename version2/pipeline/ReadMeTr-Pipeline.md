# 📌 README - Pipeline Dökümantasyonu  

Bu doküman, projenin **pipeline akışını** açıklayan `ReadMeTr-Pipeline.md` dosyasıdır. 🚀

---

## 📌 ingest.py  

Bu Python skripti, **JSON dosyasındaki metin verilerini embedding vektörlerine dönüştürerek** yerel bir dizine kaydeder. Embedding işlemi için **BAAI/bge-m3** modeli kullanılmaktadır.  

---

### 🛠 **Tercih Edilme Sebepleri**  
✔ **Retrieve performansındaki yüksek başarı** (MTEB leaderboard referansı).  
✔ **Hybrid search desteği** (dense ve sparse vektörleri birlikte işleyebilir).  
✔ **Multilingual desteği**, farklı dillerde etkili performans.  
✔ **txtai kütüphanesi kullanılarak vektör veritabanı oluşturma.**  

### ⚙ **Kullanım**  

1. **Gerekli bağımlılıkları yükleyin:**  
   ```bash
   pip install -r requirements.txt
   ```

2. **Skripti çalıştırın:**  
   ```bash
   python ingest.py
   ```

3. **Embedding vektörleri nerede saklanır?**  
   - Vektörler **`indexes/`** klasörüne kaydedilir.  
   - Varsayılan olarak **`index_bge-m3_tarih`** formatında dosya oluşturulur.  
   - SQLite tabanlı bir yapı ile **txtai kütüphanesi** kullanılarak saklanır.  


## 📌 query.py  

Bu Python skripti, **kullanıcının girdiği sorguya (query) embedding çıkararak**, daha önce `ingest.py` skripti tarafından indekslenmiş vektör veritabanı üzerinde benzerlik araması (similarity search) gerçekleştirir. **txtai kütüphanesi** kullanılarak hybrid search desteklenmektedir.  

---

### 🛠 **Özellikler**  
✔ **BGE-M3 embedding modeli kullanılarak** sorgu embedding’leri üretilir.  
✔ **Hybrid search desteği** (dense ve sparse vektörlerin ağırlıklı kombinasyonu).  
✔ **Hybrid parametresi (alpha)** ile semantic ve syntactic ağırlık dengesi ayarlanabilir.  
✔ **Limit parametresi** ile döndürülecek doküman sayısı belirlenebilir.  
✔ **txtai vektör veritabanı kullanılarak** indekslenmiş belgelerle benzerlik araması yapılır.  
✔ **Sorgular interaktif olarak çalıştırılabilir** ve ilgili sonuçlar döndürülür.  

### ⚙ **Kullanım**  

1. **Skripti çalıştırın:**  
   ```bash
   python query.py
   ```

2. **Parametre girişleri:**  
   - **Hybrid parametresi (alpha):** 0.0 - 0.5 arası dense (daha çok anlam), 0.5 - 1.0 arası sparse (daha çok kelime bazlı) önceliklidir.  
   - **Limit parametresi:** Döndürülecek sonuç sayısını belirler.  
   
3. **Örnek Çıktı Formatı:**  
   ```
   Query: Dijitalleşme mali denetim sektörünü nasıl etkiliyor?
   
   File Title   : Tecrübe Konuşuyor - Hüsnü Güreli
   Transcription: Otomasyon ve yapay zeka kullanımı sayesinde...
   Score        : 0.xyzt
   ------------------------------------------------------------
   ```

---

## 📌 query_and_llm.py

Bu Python skripti, belgelerin gömme vektörleri kullanılarak elde edilmesi ve bu belgelerden alınan bağlam ile bir Büyük Dil Modeli (LLM) üzerinden sorgu yapılmasını sağlayan bir Python skriptidir. Skript, `query.py` dosyasının işlevini genişletmekte olup, ek olarak alınan belgeler ve sorgu birleştirilerek Llama3:70b modeline (Ollama üzerinden) iletilir.

### Temel Özellikler:
- **Belge İndeksleme**: `txtai` kullanarak belgeler gömme vektörleriyle indekslenir ve aranır.
- **Hibrit Arama**: Özelleştirilebilir ağırlık parametreleriyle hibrit arama desteği.
- **LLM Entegrasyonu**: Alınan belgelerden elde edilen bağlama göre Llama3:70b modeliyle cevap üretimi.
- **Bağlamsal Yanıt Üretimi**: LLM'e verilen prompt, Türkçe sistem talimatları ve belgelerden alınan bağlama göre oluşturulur.

## Gereksinimler
- Python 3.10.16
- Belge gömme ve arama için `txtai`
- Ollama (Llama3:70b modeli)
- `subprocess` ve `json` kütüphaneleri (Python'da standart)

## Nasıl Çalışır

1. **Gömme İndeksleme**:
    `EmbeddingIndexer` sınıfı, sağlanan belgelerden bir gömme vektörü indeksi oluşturmak için `txtai` kullanır. Belgeler JSON formatında sağlanır ve bu belgeler, elde edilen indeksin bir parçası olarak kaydedilir. Eğer indeks zaten mevcutsa, bir sonraki kullanımda yüklenir.

2. **Sorgulama**:
    Kullanıcı bir sorgu girdiğinde, sistem, ilgili belgeleri gömme vektörleriyle arar. Elde edilen belgeler birleştirilerek bağlam oluşturulur.

3. **LLM Entegrasyonu**:
    Skript, elde edilen bağlamı ve kullanıcı sorgusunu Llama3:70b modeline, Ollama servisi üzerinden gönderir. Model, bağlama dayalı olarak doğru ve detaylı bir yanıt üretmesi için yönlendirilir.

4. **Yanıt Üretimi**:
    Model, sağlanan bağlama göre kullanıcının sorgusunu yanıtlamak için bir çıktı üretir. Bu yanıt, ekrana yazdırılır.

## Llama3:70b Modeli Seçimi

`llama3:70b` modeli, bu proje için, Türkçe dilinde doğru ve anlamlı yanıtlar üretme konusunda yüksek performans gösterdiği için seçilmiştir. Gelişmiş dil modeli kapasitesi, sorguları doğru şekilde anlamak ve tutarlı yanıtlar üretmek için idealdir.

Ollama ile entegrasyon, model kullanımını kolaylaştırır ve yerel model altyapısının yönetim zorluklarından kaçınılmasını sağlar, böylece daha verimli bir dağıtım sağlar.

## Skript Açıklaması

### `EmbeddingIndexer` Sınıfı

- **`__init__(self, model_name="BAAI/bge-m3", cuda_device="1")`**:
    Belirtilen model ve CUDA ayarları ile indeksleme işlemine başlar.
  
- **`load_data(self, json_file)`**:
    JSON dosyasından belgeleri yükler ve indekslemeye hazır hale getirir.
  
- **`prepare_documents(self)`**:
    Belgeleri, başlıklar ve transkriptlerle birleştirerek indekslemeye uygun hale getirir.
  
- **`index_documents(self)`**:
    Hazırlanan belgeleri `txtai` kullanarak indeksler.
  
- **`save_index(self, directory="indexes")`**:
    İndekslenen belgeleri belirtilen dizine kaydeder.

### `generate_response` Fonksiyonu

- **Yanıt Üretir**: Llama3:70b modeline, verilen bağlam ve sorgu iletilerek yanıt alınır. Fonksiyon, modelin sistem talimatlarına uygun bir prompt oluşturur.

### Ana Akış

1. Belgeler yüklenir veya indekslenir.
2. Kullanıcıdan gelen sorguya göre ilgili belgeler aranır.
3. Elde edilen belgelerden bağlam oluşturulur.
4. LLM'den gelen yanıt, bağlama dayalı olarak üretilir.
5. Yanıt ekrana yazdırılır.

## Kullanım

1. **Script'i Çalıştırın**:

    ```
    python query_and_llm.py
    ```

2. **İzleyin ve Yanıtı Alın**:
    - Sorgunuzu girdikten sonra hibrit arama için limit ve ağırlık parametrelerini girin.

3. **Sonuçları İnceleyin**:
    - Skript, en uygun belgeleri listeleyecek.
    - Ardından, LLM'den gelen yanıtı gösterecektir.


