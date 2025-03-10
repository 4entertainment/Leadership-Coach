# 📌 README - Data Dökümantasyonu 

## 📌 requirements.txt  

`requirements.txt`, projenin geliştirilmesi sırasında kullanılan bağımlılıkları içeren bir dosyadır. Bu dosya, aşağıdaki komutla oluşturulur:  

```bash
pip freeze > requirements.txt
```

Bu sayede, projenin bağımlılıkları kayıt altına alınarak farklı ortamlarda tekrar yüklenebilir.  

### ⚙️ **Ortam Kurulumu**  

1. **Yeni bir Conda ortamı oluştur:**  
   ```bash
   conda create --name env_name python==3.10.16
   ```
   (`env_name` yerine oluşturmak istediğin ortamın adını yaz.)  

2. **Gerekli bağımlılıkları yükle:**  
   ```bash
   pip install -r requirements.txt
   ```

Bu adımlar, geliştirme ortamında kullanılan tüm kütüphanelerin eksiksiz olarak yeniden yüklenmesini sağlar.  

---

## 📌 download_video_audio.py  

Bu Python betiği, belirlenen bir YouTube oynatma listesinden video ve/veya ses dosyalarını indirmek için kullanılır. Kullanıcı, mp4 formatında video, mp3 formatında ses veya her ikisini birden indirebilir. İndirme işlemleri için **yt-dlp** kütüphanesi kullanılmıştır.  

---

### 🛠 **Özellikler**  
✔ Kullanıcıdan oynatma listesi URL'sini alarak ilgili içeriği indirir.  
✔ Kullanıcının seçtiği moda (video, audio veya her ikisi) göre indirme işlemi yapar.  
✔ İndirme işlemi sırasında video ve ses dosyaları uygun formatlarda kaydedilir.  
✔ Dosyalar, belirlenen dizin içinde saklanır.  

### ⚙ **Kullanım**  

1. **Skripti çalıştırın:**  
   ```bash
   python download_video_audio.py
   ```

2. **İndirme modunu seçin:**  
   - `video` → Sadece video indirir (mp4 formatında).  
   - `audio` → Sadece ses indirir (mp3 formatında).  
   - `both` → Hem video hem ses indirir.  

---

## 📌 audio/ Klasörü  

Bu klasör, YouTube oynatma listesinden indirilen ses dosyalarını **MP3 formatında** içerir. İlgili ses dosyaları, `download_video_audio.py` betiği kullanılarak elde edilir ve bu dizine kaydedilir.  

---

### 📂 **Klasör İçeriği**  
✔ Seçilen YouTube oynatma listesindeki videolardan çıkarılmış ses dosyaları (mp3 formatında).  
✔ Dosya adları, orijinal YouTube videolarının başlıklarına göre oluşturulur.  
✔ Her bir dosya, en yüksek kalitede ses formatında saklanır.  

---

## 📌 video/ Klasörü  

Bu klasör, YouTube oynatma listesinden indirilen **MP4 formatındaki video dosyalarını** içerir. Videoların dosya adları, ilgili YouTube videolarının başlıklarına göre oluşturulmuştur. **Büyük dosya boyutları nedeniyle bu klasör GitHub'a yüklenmemiştir.**  

---

### 📂 **Klasör İçeriği**  
✔ Seçilen YouTube oynatma listesindeki videoların **MP4 formatında** indirilmiş halleri.  
✔ Dosya adları, orijinal YouTube video başlıklarına göre belirlenmiştir.  
✔ **Depolama alanı ve GitHub kısıtlamaları nedeniyle bu klasör versiyon kontrol sistemine dahil edilmemiştir.**  
✔ **Bundan sonraki veri işleme aşamaları audio-to-text olarak devam edilmiştir. Video klasörü yerine audio klasörü tercih edilmiştir.**  

**Not:** Videoları indirmek için `download_video_audio.py` betiğini kullanabilirsiniz.  

---

## 📌 video/ Klasörü  

Bu klasör, YouTube oynatma listesinden indirilen **MP4 formatındaki video dosyalarını** içerir. Videoların dosya adları, ilgili YouTube videolarının başlıklarına göre oluşturulmuştur. **Büyük dosya boyutları nedeniyle bu klasör GitHub'a yüklenmemiştir.**  

---

### 📂 **Klasör İçeriği**  
✔ Seçilen YouTube oynatma listesindeki videoların **MP4 formatında** indirilmiş halleri.  
✔ Dosya adları, orijinal YouTube video başlıklarına göre belirlenmiştir.  
✔ **Depolama alanı ve GitHub kısıtlamaları nedeniyle bu klasör versiyon kontrol sistemine dahil edilmemiştir.**  
✔ **Bundan sonraki veri işleme aşamaları audio-to-text olarak devam edilmiştir. Video klasörü yerine audio klasörü tercih edilmiştir.**  


---

## 📌 rename_or_revert_video_audio.py  

Bu Python betiği, **video (MP4) ve/veya ses (MP3) dosyalarının yeniden adlandırılması (rename) veya eski haline döndürülmesi (revert) işlemlerini** otomatikleştirir. Kullanıcı, işlem yapmak istediği dosya türünü ve dönüştürme seçeneğini belirleyebilir.  

---

### 🛠 **Özellikler**  
✔ Kullanıcının seçimine göre **dosya isimlerini temizler ve yeniden adlandırır**.  
✔ **Türkçe karakterleri opsiyonel olarak İngilizce'ye dönüştürebilir**.  
✔ **Dosya ismi değişikliklerini bir JSON dosyasında saklar** ve geri alma işlemlerine olanak tanır.  
✔ Kullanıcı, **video (MP4), ses (MP3) veya her ikisi** üzerinde işlem yapabilir.  
✔ **Dosya isimlerinde belirli karakterleri temizleyerek** düzenli bir adlandırma formatı sunar.  
✔ Yeniden adlandırılan dosyaları eski haline döndürme (revert) özelliğine sahiptir.  

### ⚙ **Kullanım**  

1. **Skripti çalıştırın:**  
   ```bash
   python rename_or_revert_video_audio.py
   ```

2. **İşlem türünü seçin:**  
   - `1` → **Dosya isimlerini temizleyip yeniden adlandırma (rename)**  
   - `2` → **Önceki isimlere geri döndürme (revert)**  

3. **Hangi dosyalar üzerinde işlem yapılacağını seçin:**  
   - `audio` → **Sadece MP3 dosyaları işlenir**  
   - `video` → **Sadece MP4 dosyaları işlenir**  
   - `both` → **Hem MP3 hem MP4 dosyaları işlenir**  

---
## 📌 audio_to_text.py & audio_to_text_no_cut.py  

Bu Python betikleri, **OpenAI Whisper Large v3** modeli kullanılarak ses dosyalarını (MP3) metne dönüştürür. **İki farklı transkripsiyon yöntemi** sunmaktadır:  
- **`audio_to_text.py`** → Ses dosyalarını **belirli uzunluklarda parçalara ayırarak** (cut) işler.  
- **`audio_to_text_no_cut.py`** → Ses dosyasını **tamamen işler** ve metni birleştirir (cut uygulanmaz).  

---

### 🛠 **Özellikler**  
✔ **OpenAI Whisper Large v3 modeli** kullanılarak yüksek doğrulukta transkripsiyon sağlar.  
✔ **İki farklı işleme yöntemi**: Parçalı transkripsiyon (**cut**) veya tam transkripsiyon (**no cut**).  
✔ **Türkçe dil desteğiyle transkripsiyon gerçekleştirir.**  
✔ **MP3 dosyalarını tek kanallı (mono) hale getirir ve 16kHz'e yeniden örnekler.**  
✔ **Her bir ses parçası için zaman damgaları ekler (cut yönteminde).**  
✔ **Sonuçları JSON formatında saklar.**  
✔ **Beam Search ve Attention Mask gibi teknikler ile modelin doğruluğunu artırır.**  

### ⚙ **Kullanım**  

1. **Skripti çalıştırın:**  
   **Parçalı transkripsiyon için (cut yöntemi)**:  
   ```bash
   python audio_to_text.py
   ```
   **Tam transkripsiyon için (no cut yöntemi)**:  
   ```bash
   python audio_to_text_no_cut.py
   ```

2. **İşlenen dosyaların kaydedildiği JSON dosyası:**  
   - `audio_to_text.py` çıktıları **`transcriptions.json`** dosyasına kaydedilir.  
   - `audio_to_text_no_cut.py` çıktıları **`transcriptions-no-cut.json`** dosyasına kaydedilir.  
   - JSON dosyaları, her ses dosyasına ait **orijinal dosya adı, transkript edilen metin ve (cut yönteminde) zaman damgalarını** içerir.  

---

## 📌 Kullanılan Model: Whisper Large v3  

- **Model:** OpenAI **Whisper Large v3**  
- **Dil:** Türkçe (`tr`)  
- **İşleme Türü:** **FP16 (float16) hassasiyetinde GPU hızlandırmalı transkripsiyon**  
- **Ses Örnekleme Frekansı:** 16kHz  
- **Çıktı Biçimi:** JSON  

---

## 📌 audio_to_text_elevenlabs.py  

Bu Python betiği, **ElevenLabs tarafından sağlanan Speech-to-Text modeli** kullanılarak ses dosyalarını (MP3) metne dönüştürür. **Çalıştırmak için bir API anahtarına (API Key) ihtiyaç duyar** ve bu anahtar `.env` dosyasında saklanmalıdır.  

---

### 🛠 **Özellikler**  
✔ **ElevenLabs `scribe_v1` modeli kullanılarak transkripsiyon sağlar.**  
✔ **Türkçe (`tur`) dilinde konuşmaları metne çevirir.**  
✔ **Konuşmacı ayrımı (diarization) yapabilir** ve farklı sesleri belirleyebilir.  
✔ **Gülme, alkış gibi olayları etiketleyebilir (optional).**  
✔ **Sonuçları JSON formatında kaydeder.**  
✔ **API anahtarı `.env` dosyasında güvenli şekilde saklanır.**  

### ⚙ **Kullanım**  

1. **API Anahtarınızı `.env` dosyanıza ekleyin:**  
   `.env` dosyanız şu formatta olmalıdır:  
   ```env
   ELEVENLABS_API_KEY=your_api_key_here
   ```

2. **Skripti çalıştırın:**  
   ```bash
   python audio_to_text_elevenlabs.py
   ```

3. **İşlenen dosyaların kaydedildiği JSON dosyası:**  
   - Varsayılan olarak **`output.json`** dosyasına kaydedilir.  
   - JSON dosyası, her ses dosyasına ait **orijinal dosya adı, transkript edilen metin ve konuşmacı ayrımı bilgilerini** içerir.  

---

## 📌 dataset/ Klasörü  

Bu klasör, **ilgili YouTube oynatma listesinden alınan ses dosyalarının metne dönüştürülmüş halleri** ile ilgili JSON formatında transkript verilerini içerir.  

---

### 📂 **Klasör İçeriği**  
✔ **`transcriptions.json`** → Transkript verileri **saniyeye bağlı chunk'lar halinde bölünmüş** şekilde saklanır.  
✔ **`transcriptions-no-cut.json`** → **Tüm transkript birleşik halde** saklanır, chunk'lara ayrılmaz.  
✔ **Her iki dosya**, **dosya isimlerini ve ilgili transkriptleri JSON formatında içerir**.  
✔ **Chunk bazlı transkripsiyon** ileride regex ile zaman aralığı bazlı analizler yapmak için kullanılabilir.  

---

