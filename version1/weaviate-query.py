import weaviate
from FlagEmbedding import BGEM3FlagModel


def main():
    # **Weaviate'e bağlan**
    try:
        client = weaviate.connect_to_local(host="localhost", port=8080)
    except Exception as e:
        print(f"HATA: Weaviate'e bağlanılamadı. ({e})")
        return

    try:
        # **Koleksiyonu tanımla**
        transcript_collection = client.collections.get("Transcript")

        # **Modeli yükle**
        model = BGEM3FlagModel("BAAI/bge-m3", use_fp16=True)

        # **Kullanıcıdan sorgu ve arama türü al**
        query_text = input("Arama yapmak istediğiniz sorguyu giriniz: ").strip()
        search_field = input("Hangi alanda aramak istersiniz? (file_title/transkript): ").strip()

        if search_field not in ["file_title", "transkript"]:
            print("Geçersiz arama alanı seçildi.")
            return

        # **BGE-M3 Modelinden Query için Embedding Çıkar**
        query_embeddings = model.encode([query_text], return_dense=True, return_sparse=True)

        dense_embedding = query_embeddings["dense_vecs"][0].tolist()

        # Sparse embedding varsa al, yoksa None olarak belirle
        sparse_embedding = query_embeddings.get("sparse_vecs", [[]])
        sparse_embedding = sparse_embedding[0].tolist() if sparse_embedding and sparse_embedding[0] else None

        # **Hybrid Search Kullanımı**
        search_params = {
            "query": query_text,  # String formatında sorgu
            "vector": dense_embedding,  # Dense vektör
            "limit": 3,
            "return_properties": ["file_title", "transkript"]
        }

        # Eğer sparse embedding mevcutsa, hybrid search'e dahil et
        if sparse_embedding:
            search_params["sparse_vector"] = sparse_embedding  # `sparse_vector` kullanıldı
        else:
            print("Uyarı: Sparse embedding bulunamadı, yalnızca dense vector kullanılacak.")

        # **Weaviate Hybrid Query Çalıştır**
        response = transcript_collection.query.hybrid(**search_params)

        # **Sonuçları yazdır**
        print("\nEn alakalı sonuçlar:")
        for idx, item in enumerate(response.objects):
            file_title = item.properties.get("file_title", "N/A")
            transkript = item.properties.get("transkript", "N/A")

            print(f"\nSonuç {idx + 1}:")
            print(f"Başlık: {file_title}")
            print(f"Transkript: {transkript}")

    except Exception as e:
        print(f"Sorgu sırasında hata oluştu: {e}")

    finally:
        # **Bağlantıyı kapat**
        client.close()


if __name__ == '__main__':
    main()

"""
    "Minidrone Yarışması 2024 Röportaj Serisi ｜ Canan Akay.mp3": {
        "file_title": "Minidrone Yarışması 2024 Röportaj Serisi ｜ Canan Akay",
        "transkript": "Merhabalar hocam, Minidrone etkinliğimize hoşgeldiniz. Merhaba, hoşbulduk. Sizlere birkaç sorum olacak. İlk sorumu kendinize tanıtır mısınız? Bu yarışmadaki göreviniz nedir? Ben İstanbul Üniversitesi Cevrahpaşa'da öğretim görevlisi doktoru olarak çalışıyorum. Kontrol Otomasyon Programı'nda. Jüri üyesi olarak yerişimeye katıldım. Hoş geldiniz tekrardan. MINIDRONE Yarışması hakkında neler düşünüyorsunuz? MINİDRONELER aslında günümüzdeki teknolojilerde birçok alanda kullanıldığını görüyoruz.  Çok teşekkür ederim hocam. Aslında son sorum Mindro yarışmasına öğrencilerin katılması onlara iş hayatlarına ne gibi kazanımlar katardı?"
    },
"""
#  İstanbul Üniversitesi Cerrahpaşa öğretim üyesi kimdir?