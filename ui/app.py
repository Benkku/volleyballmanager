from flask import Flask, render_template, request, jsonify
import random
import traceback

app = Flask(__name__, static_folder="static", template_folder="templates")

# Try to import your real simulator. If it's not available, fall back to a mock so the UI is usable immediately.
SIMULATOR_AVAILABLE = False
try:
    # Expected function signature: simulate_match(settings: dict) -> dict
    # where the returned dict contains at least {'sets': [...], 'winner': str, 'events': [...]}
    from volleyballmanager.simulator import simulate_match  # type: ignore
    SIMULATOR_AVAILABLE = True
except Exception:
    simulate_match = None  # type: ignore


def simulate_match_mock(settings: dict) -> dict:
    """
    Minimal mock simulator to let the UI work without the real simulator.
    Simulates sets in which each point is awarded randomly based on 'strength' values.
    """
    team_a = settings.get("teamA", {"name": "Team A", "strength": 5})
    team_b = settings.get("teamB", {"name": "Team B", "strength": 5})
    sets_to = int(settings.get("sets_to", 3))

    score_a_sets = 0
    score_b_sets = 0
    events = []
    set_scores = []

    while score_a_sets < sets_to and score_b_sets < sets_to:
        target = 25
        pa = max(1, float(team_a.get("strength", 5)))
        pb = max(1, float(team_b.get("strength", 5)))

        points_a = 0
        points_b = 0
        # Play a set until someone reaches target with 2-point lead
        while True:
            p_a = pa / (pa + pb)
            if random.random() < p_a:
                points_a += 1
                events.append(f"{team_a['name']} scored ({points_a}-{points_b})")
            else:
                points_b += 1
                events.append(f"{team_b['name']} scored ({points_a}-{points_b})")
            if (points_a >= target or points_b >= target) and abs(points_a - points_b) >= 2:
                break

        set_scores.append({"a": points_a, "b": points_b})
        if points_a > points_b:
            score_a_sets += 1
        else:
            score_b_sets += 1

    winner = team_a["name"] if score_a_sets > score_b_sets else team_b["name"]
    return {"sets": set_scores, "winner": winner, "events": events}


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/run", methods=["POST"])
def api_run():
    """
    Accepts JSON:
    {
      "teamA": {"name": "A", "strength": 6},
      "teamB": {"name": "B", "strength": 5},
      "sets_to": 3
    }
    Returns JSON result from simulator (or mock).
    """
    try:
        settings = request.get_json(force=True) or {}
        if SIMULATOR_AVAILABLE and simulate_match is not None:
            try:
                result = simulate_match(settings)
            except Exception:
                # If real simulator fails, return error trace for debugging.
                return jsonify({"error": "Simulator error", "trace": traceback.format_exc()}), 500
        else:
            result = simulate_match_mock(settings)

        return jsonify({"ok": True, "result": result})
    except Exception:
        return jsonify({"ok": False, "error": "Invalid request", "trace": traceback.format_exc()}), 400


if __name__ == "__main__":
    # For local development only. Use a WSGI server in production.
    app.run(host="0.0.0.0", port=5000, debug=True)
