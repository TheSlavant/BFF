from humeai_assistant import Assistant
import dotenv
import os
dotenv.load_dotenv()
HUMEAI_API_KEY = os.getenv("HUMEAI_API_KEY")

def start_conversation():
    assistant = Assistant(api_key=HUMEAI_API_KEY)
    audio_device = assistant.detect_audio_device()
    assistant.start_conversation(tts="hume_ai", device=audio_device, system_prompt="prompt.txt")

if __name__ == "__main__":
    start_conversation()