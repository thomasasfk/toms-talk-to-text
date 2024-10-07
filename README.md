# Tom's Talk-to-Text

A compact tool to convert speech to text, available as a standalone executable and a Flask web application.

## Image

![image](https://github.com/user-attachments/assets/61123245-2f7b-43cb-a5e0-0213c869e36a)

## Features

- Convert speech to text
- Powered by OpenAI's Whisper API
- Auto-copy transcription to clipboard (standalone version)
- Optional auto-paste functionality (standalone version)
- Web interface for easy access (Flask version)

## Standalone Version

### Setup

1. Download `tttt.exe` from the releases page
2. Run `tttt.exe`
3. Configure settings on first run or by clicking the "Settings" button
4. Press `Ctrl + Shift + >` to start/stop recording

### Usage

1. Press `Ctrl + Shift + >` to start recording
2. Speak clearly into your microphone
3. Press `Ctrl + Shift + >` again to stop recording and start transcription
4. The transcribed text will be copied to your clipboard (and optionally pasted)

### Configuration

- Click the "Settings" button to configure:
  - OpenAI API Key
  - Max recording duration

## Flask Web Application Version

### Setup

1. Clone the repository:
   ```
   git clone https://github.com/thomasasfk/toms-talk-to-text.git
   cd toms-talk-to-text
   ```
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Run the Flask app:
   ```
   python app.py
   ```
4. Open a web browser and navigate to `http://localhost:5000`

### Usage

1. Enter your OpenAI API key in the settings
2. Click "Start Recording" to begin
3. Speak clearly into your microphone
4. Click "Stop Recording" to end recording and start transcription
5. The transcribed text will appear in the text area

## Building the Standalone Version from Source (Optional)

1. Install Python 3.10
2. Clone the repository and navigate to the project directory
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

- For the standalone version, settings are stored in a local `settings.json` file in the user's data directory.
- For the Flask version, the OpenAI API key is entered in the web interface and not stored permanently.

## Security Considerations

Always keep your OpenAI API key confidential. In the Flask version, ensure you're running the application on a secure network, as the API key is transmitted with each request.