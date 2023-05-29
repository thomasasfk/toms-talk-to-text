from __future__ import annotations

import os
import tempfile
import threading
import time
import wave

import keyboard
import openai
import pyaudio
import pyautogui
import pyperclip
from dotenv import load_dotenv

load_dotenv()

RECORDING = False

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100

audio = pyaudio.PyAudio()
stream = audio.open(
    format=FORMAT, channels=CHANNELS,
    rate=RATE, input=True, frames_per_buffer=CHUNK,
)


def handle_key_event(e: keyboard.KeyboardEvent) -> None:
    global RECORDING

    if not all([e.name == '>', keyboard.is_pressed('ctrl'), keyboard.is_pressed('shift')]):
        return

    if RECORDING := not RECORDING:
        print('Ctrl+Shift+. pressed! Starting recording...')
        record_thread = threading.Thread(target=handle_recording)
        record_thread.start()


def handle_recording() -> None:
    frames = []
    start_time = time.time()

    while RECORDING:
        data = stream.read(CHUNK)
        frames.append(data)

        elapsed_time = time.time() - start_time
        max_seconds = int(os.getenv('MAX_RECORDING_SECONDS', '300')) # 5 minutes = 300 seconds
        if elapsed_time >= max_seconds:
            print('Recording time limit reached.')
            RECORDING = False
    print('Recording stopped.')

    filename = save_audio(frames)
    print('Audio saved. File:', filename)

    transcript = get_transcript_from_open_ai_whisper(filename)
    text = transcript.get('text') or 'Error.. :('
    print('Text:', text)

    pyperclip.copy(text)
    time.sleep(0.1)
    pyautogui.hotkey('ctrl', 'v')

    os.remove(filename)


def save_audio(frames) -> str:
    temp_dir = tempfile.mkdtemp()
    temp_file = tempfile.NamedTemporaryFile(
        suffix='.wav', dir=temp_dir, delete=False,
    )

    wave_file = wave.open(temp_file.name, 'wb')
    wave_file.setnchannels(CHANNELS)
    wave_file.setsampwidth(audio.get_sample_size(FORMAT))
    wave_file.setframerate(RATE)
    wave_file.writeframes(b''.join(frames))
    wave_file.close()

    name = temp_file.name
    temp_file.close()

    return name


def get_transcript_from_open_ai_whisper(filepath: str):
    audio_file = open(filepath, 'rb')
    transcript = openai.Audio.transcribe('whisper-1', audio_file)
    return transcript


def main():
    openai.api_key = os.getenv('OPENAI_API_KEY') or input('OpenAI API key: ')
    keyboard.on_press(handle_key_event)
    keyboard.wait()


if __name__ == '__main__':
    raise SystemExit(main())
