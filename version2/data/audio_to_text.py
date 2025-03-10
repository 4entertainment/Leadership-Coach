import os
import json
import torch
import numpy as np
from transformers import WhisperForConditionalGeneration, WhisperProcessor
from pydub import AudioSegment


class WhisperTranscriber:
    """
    A class to handle audio transcription using OpenAI's Whisper model.
    """

    def __init__(self, model_name="openai/whisper-large-v3", audio_chunk_length=60):
        """
        Initializes the Whisper model and processor.
        """
        print(f"GPU Available: {torch.cuda.is_available()}")
        self.model_name = model_name
        self.audio_chunk_length = audio_chunk_length
        
        # Load Whisper model
        self.whisper_model = WhisperForConditionalGeneration.from_pretrained(
            self.model_name, torch_dtype=torch.float16, device_map={"": 0}
        )
        self.whisper_processor = WhisperProcessor.from_pretrained(self.model_name)

    def load_mp3(self, audio_path, target_sample_rate=16000):
        """
        Loads an MP3 file, converts it to mono, and resamples it to the target sample rate.
        """
        audio = AudioSegment.from_mp3(audio_path)
        audio = audio.set_channels(1)  # Convert to mono
        audio = audio.set_frame_rate(target_sample_rate)  # Resample to 16kHz
        samples = np.array(audio.get_array_of_samples()).astype(np.float32)
        max_val = float(2 ** (8 * audio.sample_width - 1))
        samples = samples / max_val
        return torch.tensor(samples)

    def chunk_audio(self, audio_path):
        """
        Splits the audio into smaller chunks of predefined length.
        """
        speech = self.load_mp3(audio_path, target_sample_rate=16000)
        sr = 16000
        num_samples_per_chunk = self.audio_chunk_length * sr
        chunks, timestamps = [], []
        
        for i in range(0, len(speech), num_samples_per_chunk):
            chunks.append(speech[i:i + num_samples_per_chunk])
            timestamps.append(i / sr)
        
        return chunks, timestamps

    def transcribe_chunk(self, chunk):
        """
        Transcribes a given audio chunk in Turkish using the Whisper model.
        """
        inputs = self.whisper_processor(chunk, return_tensors="pt", sampling_rate=16000)
        inputs["input_features"] = inputs["input_features"].to(self.whisper_model.device, torch.float16)
        
        with torch.no_grad():
            predicted_ids = self.whisper_model.generate(
                inputs["input_features"],
                no_repeat_ngram_size=2,
                language="tr"
            )
        
        return self.whisper_processor.batch_decode(predicted_ids, skip_special_tokens=True)[0]

    def transcribe_mp3(self, audio_path):
        """
        Transcribes an entire MP3 file by splitting it into chunks and processing each one.
        """
        full_transcription = []
        chunks, timestamps = self.chunk_audio(audio_path)
        
        for chunk, start_time in zip(chunks, timestamps):
            transcription = self.transcribe_chunk(chunk)
            timestamp_str = f"[{start_time:.2f}s - {start_time + self.audio_chunk_length:.2f}s]"
            full_transcription.append(f"{timestamp_str} {transcription}")
        
        return full_transcription

    def transcribe_folder(self, input_folder, output_json):
        """
        Processes all MP3 files in a folder and saves the transcriptions as a JSON file.
        """
        mp3_files = [os.path.join(input_folder, f) for f in os.listdir(input_folder) if f.lower().endswith(".mp3")]
        print(f"Found MP3 files: {mp3_files}")
        results = {}

        for mp3_file in mp3_files:
            print(f"Processing: {mp3_file} ...")
            transcription = self.transcribe_mp3(mp3_file)
            base_name = os.path.basename(mp3_file)
            title = os.path.splitext(base_name)[0]

            results[base_name] = {
                "file_title": title,
                "transcription": transcription
            }
        
        with open(output_json, "w", encoding="utf-8") as f:
            json.dump(results, f, ensure_ascii=False, indent=4)
        
        print(f"Transcription results saved to {output_json}")


if __name__ == "__main__":
    # Paths for input folder and output JSON file
    mp3_folder = "./audio"
    output_json = "transcriptions.json"
    
    # Create an instance of WhisperTranscriber and process the MP3 folder
    transcriber = WhisperTranscriber()
    transcriber.transcribe_folder(mp3_folder, output_json)
