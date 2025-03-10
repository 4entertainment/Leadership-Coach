import os
import json
from dotenv import load_dotenv
from io import BytesIO
from elevenlabs.client import ElevenLabs

# Load environment variables from a .env file
load_dotenv()

# Initialize the ElevenLabs client with your API key
client = ElevenLabs(
    api_key=os.getenv("ELEVENLABS_API_KEY"),
)

def transcribe_file(file_path):
    """
    Transcribe a single audio file using the ElevenLabs speech_to_text.convert method.
    """
    with open(file_path, "rb") as audio_file:
        audio_data = BytesIO(audio_file.read())
        transcription = client.speech_to_text.convert(
            file=audio_data,
            model_id="scribe_v1",          # or "scribe_v1_base" if you prefer
            tag_audio_events=True,         # Optionally tag events like laughter, applause, etc.
            language_code="tur",           # Set language to Turkish
            diarize=True,                  # Whether to annotate who is speaking
        )
        return transcription.text

def preprocess_audio_files(directory):
    """
    Process all MP3 files in the given directory, returning a dictionary
    where the key is the filename and the value is another dictionary containing
    the file_title and its transcription.
    """
    results = {}
    for filename in os.listdir(directory):
        if filename.lower().endswith(".mp3"):
            file_path = os.path.join(directory, filename)
            file_title = os.path.splitext(filename)[0]
            print(f"Processing: {filename}")
            try:
                transcription_text = transcribe_file(file_path)
                results[filename] = {
                    "file_title": file_title,
                    "transcription": transcription_text
                }
            except Exception as e:
                print(f"Error processing {filename}: {e}")
    return results

if __name__ == "__main__":
    # Specify the directory containing your MP3 files
    directory = "/data/Workspace/balkan/leadership_coach/data_preprocess/audio"  # Replace with your folder path
    
    data = preprocess_audio_files(directory)
    
    # Write the results to a JSON file
    with open("output.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    
    print("Transcriptions have been saved to output.json")
