import weaviate
import torch
from FlagEmbedding import BGEM3FlagModel
from transformers import AutoTokenizer, AutoModelForCausalLM
from transformers import BitsAndBytesConfig

model_id = "malhajar/Mistral-7B-Instruct-v0.2-turkish"
# model_id = "tensorblock/Mistral-7B-Instruct-v0.2-turkish-GGUF"
# with llama.cpp ::: model_id = "matrixportal/Turkish-Llama-8b-DPO-v0.1-Q4_K_M-GGUF"

quantization_config = BitsAndBytesConfig(
    load_in_4bit=True,  # Modeli 8-bit modda yükle
    bnb_8bit_compute_dtype=torch.float16,  # Hesaplamaları fp16 ile yap
    bnb_8bit_use_double_quant=True  # Çift quantization kullan
)

model = AutoModelForCausalLM.from_pretrained(model_id,
                                             quantization_config=quantization_config,
                                             device_map="auto",
                                             torch_dtype=torch.float16,
                                             revision="main")
model.eval()
tokenizer = AutoTokenizer.from_pretrained(model_id)


def generate_response(context, query_text):
    """LLM ile RAG yanıtı üretir"""
    prompt = f"""
### Instruction: 
Aşağıda verilen bağlamdaki bilgileri kullanarak '{query_text}' sorusuna uygun ve detaylı bir yanıt ver.

### Context:
{context}

### Response:
"""
    input_ids = tokenizer(prompt, return_tensors="pt").input_ids.to(model.device)

    output = model.generate(inputs=input_ids, max_new_tokens=512,
                            pad_token_id=tokenizer.eos_token_id,
                            top_k=50, do_sample=True,
                            repetition_penalty=1.3, top_p=0.95)

    response = tokenizer.decode(output[0], skip_special_tokens=True)
    return response

"""
original llm template:
### Instruction:

<prompt> (without the <>)

### Response:
"""
def main():
    try:
        client = weaviate.connect_to_local(host="localhost", port=8080)
    except Exception as e:
        print(f"HATA: Weaviate'e bağlanılamadı. ({e})")
        return

    try:
        transcript_collection = client.collections.get("Transcript")

        model_bge = BGEM3FlagModel("BAAI/bge-m3", use_fp16=True)

        query_text = input("Arama yapmak istediğiniz sorguyu giriniz: ").strip()
        search_field = input("Hangi alanda aramak istersiniz? (file_title/transkript): ").strip()

        if search_field not in ["file_title", "transkript"]:
            print("Geçersiz arama alanı seçildi.")
            return

        query_embeddings = model_bge.encode([query_text], return_dense=True, return_sparse=True)

        dense_embedding = query_embeddings["dense_vecs"][0].tolist()

        sparse_embedding = query_embeddings.get("sparse_vecs", [[]])
        sparse_embedding = sparse_embedding[0].tolist() if sparse_embedding and sparse_embedding[0] else None

        search_params = {
            "query": query_text,
            "vector": dense_embedding,
            "limit": 1,
            "return_properties": ["file_title", "transkript"]
        }

        if sparse_embedding:
            search_params["sparse_vector"] = sparse_embedding
        else:
            print("Uyarı: Sparse embedding bulunamadı, yalnızca dense vector kullanılacak.")

        response = transcript_collection.query.hybrid(**search_params)

        context_pieces = []
        for idx, item in enumerate(response.objects):
            file_title = item.properties.get("file_title", "N/A")
            transkript = item.properties.get("transkript", "N/A")
            context_pieces.append(f"Başlık: {file_title}\nTranskript: {transkript}")

        context = "\n\n".join(context_pieces)
        # print("saghdqwbdqwvqgwdjq\n\n" + context)
        # quit()
        if not context_pieces:
            print("Weaviate'de ilgili sonuç bulunamadı.")
            return

        final_response = generate_response(context, query_text)

        print("\n### LLM Yanıtı ###\n")
        print(final_response)

    except Exception as e:
        print(f"Sorgu sırasında hata oluştu: {e}")

    finally:
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
