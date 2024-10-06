import os
import sys
import tempfile
import threading
import time
import wave
import json
from typing import Dict, Any

import keyboard
import openai
import pyaudio
import pyperclip
import pyautogui
from tkinter import Tk, Label, StringVar, Checkbutton, BooleanVar, Entry, Toplevel, Button, Frame
from appdirs import user_data_dir

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100

APP_NAME = "TomsTalkToText"
APP_AUTHOR = "thomasaf"

class TalkToTextApp:
    def __init__(self):
        self.recording = False
        self.settings = self.load_settings()
        self.setup_ui()

    @staticmethod
    def resource_path(path: str) -> str:
        try:
            return os.path.join(sys._MEIPASS, path)
        except Exception:
            return os.path.join(os.path.abspath("."), path)

    @staticmethod
    def get_settings_path() -> str:
        data_dir = user_data_dir(APP_NAME, APP_AUTHOR)
        os.makedirs(data_dir, exist_ok=True)
        return os.path.join(data_dir, 'settings.json')

    def load_settings(self) -> Dict[str, Any]:
        settings_path = self.get_settings_path()
        try:
            with open(settings_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {"openai_api_key": "", "max_recording_seconds": 300}

    def save_settings(self) -> None:
        settings_path = self.get_settings_path()
        with open(settings_path, 'w') as f:
            json.dump(self.settings, f)

    def setup_ui(self) -> None:
        self.root = Tk()
        self.root.title("Tom's Talk to Text")
        self.root.geometry("350x150")
        self.root.resizable(False, False)
        icon_path = self.resource_path('icon.ico')
        self.root.iconbitmap(icon_path)

        main_frame = Frame(self.root, padx=10, pady=10)
        main_frame.pack(fill='both', expand=True)

        self.status_var = StringVar()
        self.status_var.set("Press Ctrl+Shift+> to start recording")

        status_label = Label(main_frame, textvariable=self.status_var, anchor='w', justify='left')
        status_label.pack(fill='x', pady=(0, 10))

        self.paste_after_transcribe = BooleanVar(value=True)
        paste_checkbox = Checkbutton(main_frame, text="Paste after transcription", variable=self.paste_after_transcribe, anchor='w')
        paste_checkbox.pack(fill='x')

        settings_button = Button(main_frame, text="Settings", command=self.open_settings)
        settings_button.pack(side='right', anchor='se', pady=(10, 0))

        keyboard.on_press(self.toggle_recording)

    def toggle_recording(self, e: keyboard.KeyboardEvent = None) -> None:
        if all([e.name == '>', keyboard.is_pressed('ctrl'), keyboard.is_pressed('shift')]):
            self.recording = not self.recording
            self.status_var.set('Recording started...' if self.recording else 'Recording stopped.')
            if self.recording:
                threading.Thread(target=self.record_and_transcribe).start()

    def record_and_transcribe(self) -> None:
        frames, start_time = [], time.time()
        p = pyaudio.PyAudio()
        try:
            stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)
            while self.recording and time.time() - start_time < self.settings['max_recording_seconds']:
                frames.append(stream.read(CHUNK))
        finally:
            if 'stream' in locals():
                stream.stop_stream()
                stream.close()
            p.terminate()

        self.status_var.set("Processing audio...")
        with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as temp_file:
            with wave.open(temp_file.name, 'wb') as wf:
                wf.setnchannels(CHANNELS)
                wf.setsampwidth(p.get_sample_size(FORMAT))
                wf.setframerate(RATE)
                wf.writeframes(b''.join(frames))
            self.status_var.set('Transcribing...')
            with open(temp_file.name, 'rb') as audio_file:
                try:
                    text = openai.Audio.transcribe('whisper-1', audio_file).get('text', 'Error.. :(')
                except Exception as e:
                    self.status_var.set(f"Error: {str(e)}")
                    return

        pyperclip.copy(text)
        self.status_var.set('Transcription complete. Copied to clipboard.')
        if self.paste_after_transcribe.get():
            pyautogui.hotkey('ctrl', 'v')
        os.remove(temp_file.name)
        self.root.after(5000, lambda: self.status_var.set("Press Ctrl+Shift+> to start recording"))

    def open_settings(self) -> None:
        settings_window = Toplevel(self.root)
        settings_window.title("Settings")
        settings_window.geometry("400x200")
        settings_window.iconbitmap(self.resource_path('icon.ico'))
        settings_window.grab_set()

        settings_frame = Frame(settings_window, padx=10, pady=10)
        settings_frame.pack(fill='both', expand=True)

        Label(settings_frame, text="OpenAI API Key:", anchor='w').pack(fill='x', pady=(0, 5))
        api_key_entry = Entry(settings_frame, width=40)
        api_key_entry.insert(0, self.settings['openai_api_key'])
        api_key_entry.pack(fill='x', pady=(0, 10))

        Label(settings_frame, text="Max Recording Seconds:", anchor='w').pack(fill='x', pady=(0, 5))
        max_seconds_entry = Entry(settings_frame, width=10)
        max_seconds_entry.insert(0, str(self.settings['max_recording_seconds']))
        max_seconds_entry.pack(anchor='w', pady=(0, 10))

        def save():
            self.settings['openai_api_key'] = api_key_entry.get()
            self.settings['max_recording_seconds'] = int(max_seconds_entry.get())
            self.save_settings()
            openai.api_key = self.settings['openai_api_key']
            settings_window.destroy()

        Button(settings_frame, text="Save", command=save).pack(anchor='w')

    def run(self) -> None:
        if not self.settings['openai_api_key']:
            self.open_settings()
        openai.api_key = self.settings['openai_api_key']
        self.root.mainloop()

if __name__ == '__main__':
    app = TalkToTextApp()
    app.run()