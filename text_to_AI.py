from googletrans import Translator
from gtts import gTTS
import os

def text_to_speech_with_translation(text, source_lang, target_lang):
    # Translate text
    translator = Translator()
    translated_text = translator.translate(text, src=source_lang, dest=target_lang).text
    print(f"Translated Text: {translated_text}")

    # Convert translated text to speech
    tts = gTTS(text=translated_text, lang=target_lang)
    audio_file = 'translated_speech.mp3'
    tts.save(audio_file)
    
    # Output audio
    os.system(f"start {audio_file}")  # Use "afplay" instead of "start" on macOS, or "xdg-open" on Linux

if __name__ == "__main__":
    text = input("Enter the text to translate and convert to speech: ")
    source_lang = input("Enter the source language (e.g., 'en' for English): ")
    target_lang = input("Enter the target language (e.g., 'fr' for French): ")
    
    text_to_speech_with_translation(text, source_lang, target_lang)
