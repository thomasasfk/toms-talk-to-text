# Tom's Talk-to-Text

A compact tool to convert speech to text with a single keybind.

## Image

![image](https://github.com/user-attachments/assets/61123245-2f7b-43cb-a5e0-0213c869e36a)

## Features

- Convert speech to text with a single hotkey (`Ctrl + Shift + >`)
- Powered by OpenAI's Whisper API
- Auto-copy transcription to clipboard
- Optional auto-paste functionality

## Setup

1. Download `tttt.exe` from the releases page
2. Run `tttt.exe`
3. Configure settings on first run or by clicking the "Settings" button
4. Press `Ctrl + Shift + >` to start/stop recording

## Usage

1. Press `Ctrl + Shift + >` to start recording
2. Speak clearly into your microphone
3. Press `Ctrl + Shift + >` again to stop recording and start transcription
4. The transcribed text will be copied to your clipboard (and optionally pasted)

## Configuration

- Click the "Settings" button to configure:
  - OpenAI API Key
  - Max recording duration

## Building from Source (Optional)

1. Install Python 3.10
2. Clone the repository:
   ```
   git clone https://github.com/thomasasfk/toms-talk-to-text.git
   cd toms-talk-to-text
   ```
3. Install dependencies:
   ```
   python -m venv .venv
   . .venv/bin/activate  # On Windows use `.venv\Scripts\activate`
   pip install -r requirements.txt
   ```
4. Compile executable:
   ```
   pyinstaller --onefile --icon=icon.ico --add-data "icon.ico;." --noconsole -n=tttt main.py
   ```
5. Find the executable in the `dist` folder

## Note

Settings are stored in a local `settings.json` file in the user's data directory.
