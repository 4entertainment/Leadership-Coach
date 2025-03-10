import json
import weaviate
from FlagEmbedding import BGEM3FlagModel

def main():
    with weaviate.connect_to_local(host="localhost", port=8080) as client:
        try:
            meta = client.get_meta()
            print(f"Weaviate çalışıyor: {meta}")
        except Exception as e:
            print(f"HATA: Weaviate'e bağlanılamadı. Lütfen Docker konteynerini başlatın. ({e})")
            return

        schema = {
            "class": "Transcript",
            "properties": [
                {"name": "file_title", "dataType": ["text"]},
                {"name": "transkript", "dataType": ["text"]},
                {"name": "dense_vector", "dataType": ["number[]"]}  # Dense embedding
            ]
        }

        if not client.collections.exists("Transcript"):
            client.collections.create_from_dict(schema)
            print("Schema oluşturuldu.")
        else:
            print("Schema zaten mevcut.")

        model = BGEM3FlagModel("BAAI/bge-m3", use_fp16=True)

        data_file = "transcriptions-no-cut.json"
        with open(data_file, "r", encoding="utf-8") as f:
            data = json.load(f)

        transcript_collection = client.collections.get("Transcript")

        for _, content in data.items():
            text = content["transkript"]

            embeddings = model.encode([text], return_dense=True, return_sparse=True)

            dense_embedding = embeddings["dense_vecs"][0].tolist()

            sparse_embedding = embeddings.get("sparse_vecs", [])

            if not sparse_embedding:
                print(f"Sparse embedding bulunamadı: {content['file_title']}")

            transcript_data = {
                "file_title": content["file_title"],
                "transkript": text,
                "dense_vector": dense_embedding
            }

            if sparse_embedding:
                transcript_data["sparse_vector"] = sparse_embedding[0].tolist()

            transcript_collection.data.insert(transcript_data)
            print(f"Eklendi: {content['file_title']}")

        print("Tüm veriler başarıyla eklendi.")

if __name__ == '__main__':
    from multiprocessing import freeze_support
    freeze_support()
    main()

# to run: docker compose up -d
# python 3ingest.py
# token name: weavite-sample-1
