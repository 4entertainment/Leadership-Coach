import streamlit as st
import torch
from transformers import VitsModel, AutoTokenizer
import scipy.io.wavfile
import io
import numpy as np

@st.cache_resource
def load_model_and_tokenizer():
    model = VitsModel.from_pretrained("facebook/mms-tts-tur")
    tokenizer = AutoTokenizer.from_pretrained("facebook/mms-tts-tur")
    return model, tokenizer

model, tokenizer = load_model_and_tokenizer()

st.title("Text-to-Speech App")

text_input = st.text_area("Enter text to speak:", "türkçe konuşuyorum. birkaç şey diyorum")

if st.button("Speak"):
    with st.spinner("Generating speech..."):
        # Tokenize and run inference
        inputs = tokenizer(text_input, return_tensors="pt")
        with torch.no_grad():
            result = model(**inputs)
            waveform = result.waveform.detach().cpu().numpy()

        # Squeeze extra dimensions if present (e.g., shape: (1, n_samples))
        if waveform.ndim > 1:
            waveform = waveform.squeeze()

        # Normalize waveform to range [-1, 1] then convert to int16 range [-32767, 32767]
        waveform_norm = waveform / np.max(np.abs(waveform))
        waveform_int16 = (waveform_norm * 32767).astype(np.int16)

        sampling_rate = model.config.sampling_rate

        # Write waveform to an in-memory buffer as a WAV file
        wav_buffer = io.BytesIO()
        scipy.io.wavfile.write(wav_buffer, rate=sampling_rate, data=waveform_int16)
        wav_buffer.seek(0)

        st.success("Speech generated!")
        st.audio(wav_buffer, format="audio/wav")

# sample:
# "Merhabalar hocam, Minidrone etkinliğimize hoşgeldiniz. Merhaba, hoşbulduk. Sizlere birkaç sorum olacak. İlk sorumu kendinize tanıtır mısınız? Bu yarışmadaki göreviniz nedir? Ben İstanbul Üniversitesi Cevrahpaşa'da öğretim görevlisi doktoru olarak çalışıyorum. Kontrol Otomasyon Programı'nda. Jüri üyesi olarak yerişimeye katıldım. Hoş geldiniz tekrardan. MINIDRONE Yarışması hakkında neler düşünüyorsunuz? MINİDRONELER aslında günümüzdeki teknolojilerde birçok alanda kullanıldığını görüyoruz.  Çok teşekkür ederim hocam. Aslında son sorum Mindro yarışmasına öğrencilerin katılması onlara iş hayatlarına ne gibi kazanımlar katardı?"