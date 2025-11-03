```markdown
# Volleyball Simulator UI (ui/web-ui)

This is a minimal Flask-based UI for the volleyball simulator.

What it does
- Serves a small web interface to configure teams and run a match.
- Tries to call `volleyballmanager.simulator.simulate_match(settings)` if available.
- Falls back to a built-in mock simulator so the UI works out-of-the-box.

Quick start (local)
1. Create a Python environment and install dependencies:
   python -m venv venv
   source venv/bin/activate   # on Windows: venv\Scripts\activate
   pip install -r requirements.txt

2. Run the app:
   python app.py

3. Open http://localhost:5000 in your browser.

Notes
- Run the app from the ui directory so Flask finds templates/ and static/ relative to app.py:
  cd ui
  python -m pip install -r requirements.txt
  python app.py

- If you prefer running from the repo root, edit the top of ui/app.py:
  app = Flask(__name__, static_folder="ui/static", template_folder="ui/templates")

Next steps
- Wire the API to your real simulator if its import path or signature differs.
- Add a Dockerfile if you prefer running the UI in a container.
```
