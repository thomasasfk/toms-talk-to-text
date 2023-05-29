## toms-talk-to-text

Default keybind is: `Ctrl + Shift + .` (note the code says `>` as I am on UK keyboard, not sure if this works elsewhere.

What does this do?:

- Press keybind (start recording)
- Monologue into your microphone
- Press keybind (stop recording)
- Wait a few seconds
- What you said will be pasted as text

---

Setup:

- Install Python 3.10 (pyenv recommended)
- Copy `.env.example` to `.env`
```bash
cp .env.example .env
```

- Add OPENAI_API_KEY
```bash
python -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements.txt
```
- Run the script
```bash
python main.py
```
