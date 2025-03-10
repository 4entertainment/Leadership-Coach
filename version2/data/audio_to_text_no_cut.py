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

    def __init__(self, model_name: str = "openai/whisper-large-v3", audio_chunk_length: int = 60, target_sample_rate: int = 16000):
        """
        Initializes the Whisper model, its processor, and transcription settings.
        
        :param model_name: Identifier for the Whisper model.
        :param audio_chunk_length: Duration (in seconds) for each audio chunk.
        :param target_sample_rate: Sampling rate to use for processing audio.
        """
        print(f"GPU Available: {torch.cuda.is_available()}")
        self.audio_chunk_length = audio_chunk_length
        self.target_sample_rate = target_sample_rate
        
        # Load the Whisper model and its processor
        self.model = WhisperForConditionalGeneration.from_pretrained(
            model_name,
            torch_dtype=torch.float16,
            device_map={"": 0}  # Automatically maps model to GPU if available
        )
        self.processor = WhisperProcessor.from_pretrained(model_name)

    def load_mp3(self, audio_path: str) -> torch.Tensor:
        """
        Loads an MP3 file, converts it to mono, resamples it to the target sample rate,
        and normalizes the audio samples.
        
        :param audio_path: Path to the MP3 file.
        :return: A Torch tensor containing normalized audio samples.
        """
        audio = AudioSegment.from_mp3(audio_path)
        audio = audio.set_channels(1)  # Convert to mono
        audio = audio.set_frame_rate(self.target_sample_rate)  # Resample audio
        samples = np.array(audio.get_array_of_samples()).astype(np.float32)
        max_val = float(2 ** (8 * audio.sample_width - 1))
        samples = samples / max_val  # Normalize the samples
        return torch.tensor(samples)

    def chunk_audio(self, audio: torch.Tensor) -> list:
        """
        Splits the full audio tensor into smaller chunks.
        
        :param audio: The full audio tensor.
        :return: A list of audio chunks (Torch tensors).
        """
        num_samples_per_chunk = self.audio_chunk_length * self.target_sample_rate
        chunks = []
        for i in range(0, len(audio), num_samples_per_chunk):
            chunks.append(audio[i:i + num_samples_per_chunk])
        return chunks

    def transcribe_chunk(self, chunk: torch.Tensor) -> str:
        """
        Transcribes a single audio chunk using the Whisper model.
        
        :param chunk: A chunk of audio as a Torch tensor.
        :return: The transcription text.
        """
        inputs = self.processor(
            chunk,
            return_tensors="pt",
            sampling_rate=self.target_sample_rate,
            return_attention_mask=True  # Request attention mask for improved performance
        )
        # Move input features and attention mask to the model's device
        inputs["input_features"] = inputs["input_features"].to(self.model.device, torch.float16)
        attention_mask = inputs["attention_mask"].to(self.model.device)
        
        with torch.no_grad():
            predicted_ids = self.model.generate(
                inputs["input_features"],
                attention_mask=attention_mask,
                no_repeat_ngram_size=2,
                num_beams=5,           # Using beam search for higher-quality results
                early_stopping=True,   # Enable early stopping during generation
                language="tr"          # Set language to Turkish
            )
        # Decode the generated token IDs into text
        transcription = self.processor.batch_decode(predicted_ids, skip_special_tokens=True)[0]
        return transcription

    def transcribe_mp3(self, audio_path: str) -> str:
        """
        Transcribes an entire MP3 file by splitting it into chunks and concatenating
        the individual transcriptions.
        
        :param audio_path: The path to the MP3 file.
        :return: The full transcription text.
        """
        full_audio = self.load_mp3(audio_path)
        chunks = self.chunk_audio(full_audio)
        full_transcription = ""
        for chunk in chunks:
            transcription = self.transcribe_chunk(chunk)
            full_transcription += " " + transcription
        return full_transcription.strip()

    def transcribe_folder(self, input_folder: str, output_json: str):
        """
        Processes all MP3 files in a folder and saves the transcriptions as a JSON file.
        
        :param input_folder: Directory containing MP3 files.
        :param output_json: Path to the JSON file where transcriptions will be saved.
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
    # Paths for the input folder and output JSON file
    mp3_folder = "./audio"
    output_json = "transcriptions-no-cut.json"
    
    # Create an instance of WhisperTranscriber and process the MP3 folder
    transcriber = WhisperTranscriber()
    transcriber.transcribe_folder(mp3_folder, output_json)
