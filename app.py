import os
import tempfile
from flask import Flask, render_template, request, jsonify
import openai

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/transcribe', methods=['POST'])
def transcribe():
    if 'audio' not in request.files:
        return jsonify({'error': 'No audio file provided'}), 400

    api_key = request.headers.get('X-API-KEY')
    if not api_key:
        return jsonify({'error': 'No API key provided'}), 400

    openai.api_key = api_key

    audio_file = request.files['audio']

    with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as temp_file:
        audio_file.save(temp_file.name)

        try:
            with open(temp_file.name, 'rb') as audio:
                transcription = openai.Audio.transcribe('whisper-1', audio)

            text = transcription.get('text', 'Error occurred during transcription')
            return jsonify({'transcription': text})
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    os.remove(temp_file.name)

if __name__ == '__main__':
    app.run(debug=True)