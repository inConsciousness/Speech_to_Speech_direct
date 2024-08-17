import speech_recognition as sr
from googletrans import Translator, LANGUAGES
from gtts import gTTS
import os
from pydub import AudioSegment
from pydub.playback import play
from datetime import datetime

def speech_to_text(recognizer, audio):
    try:
        return recognizer.recognize_google(audio)
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
        return None
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")
        return None

def translate_text(text, target_lang):
    translator = Translator()
    translated_text = translator.translate(text, dest=target_lang).text
    print(f"Translated Text: {translated_text}")
    return translated_text

def text_to_speech(text, lang, filename):
    tts = gTTS(text=text, lang=lang)
    tts.save(filename)

def play_audio(file_path):
    audio = AudioSegment.from_mp3(file_path)
    play(audio)

if __name__ == "__main__":
    recognizer = sr.Recognizer()

    # Record the audio from the system's microphone
    with sr.Microphone() as source:
        print("Please speak:")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    text = speech_to_text(recognizer, audio)

    if text:
        print(f"Recognized Text: {text}")

        # Print available target languages
        print("Available target languages:")
        for lang_code, lang_name in LANGUAGES.items():
            print(f"{lang_code}: {lang_name}")

        target_lang = input("Enter the target language code: ")

        # Create a unique timestamped filename for the input and output files
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        input_dir = "audio_files"
        output_dir = "translated_audio"
        
        # Ensure directories exist
        os.makedirs(input_dir, exist_ok=True)
        os.makedirs(output_dir, exist_ok=True)

        input_filename = os.path.join(input_dir, f"input_speech_{timestamp}.wav")
        output_filename = os.path.join(output_dir, f"translated_speech_{timestamp}.mp3")

        # Save the recorded audio to a WAV file (for better compatibility with pydub)
        with open(input_filename, "wb") as f:
            f.write(audio.get_wav_data())
        print(f"Input speech saved as {input_filename}")

        # Translate the recognized text to the target language
        translated_text = translate_text(text, target_lang)

        # Convert the translated text to speech and save it to an MP3 file
        text_to_speech(translated_text, target_lang, output_filename)
        print(f"Translated speech saved as {output_filename}")

        # Play the translated audio
        play_audio(output_filename)
    else:
        print("No speech was recognized.")
