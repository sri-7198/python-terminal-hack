from flask import Flask, request, jsonify
import subprocess, tempfile, os, uuid

app = Flask(__name__)

@app.route("/local_run", methods=["POST"])
def local_run():
    """
    Simple, time-limited Python runner for hackathon demos.
    - Accepts JSON: { "language": "python", "code": "<code>" }
    - Supports only Python here (safe for demo). Limits: size and timeout.
    """
    data = request.get_json(silent=True) or {}
    language = (data.get("language") or "python").lower()
    code = data.get("code", "")

    if language != "python":
        return jsonify({"error": "Only 'python' supported by local runner"}), 400

    if not code.strip():
        return jsonify({"error": "no code provided"}), 400

    # Safety limits
    if len(code) > 20000:
        return jsonify({"error": "code too large"}), 400

    # Create temp file
    fname = f"/tmp/run_{uuid.uuid4().hex}.py"
    try:
        with open(fname, "w", encoding="utf-8") as f:
            f.write(code)

        proc = subprocess.run(
            ["python3", fname],
            capture_output=True,
            text=True,
            timeout=5  # seconds
        )

        out, err, rc = proc.stdout, proc.stderr, proc.returncode
    except subprocess.TimeoutExpired:
        out, err, rc = "", "timeout (5s)", 124
    except Exception as e:
        out, err, rc = "", f"runner error: {e}", 1
    finally:
        try:
            os.remove(fname)
        except:
            pass

    return jsonify({"stdout": out, "stderr": err, "returncode": rc})

# Entry point
if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))  # Use $PORT if set, else 5000
    app.run(host="0.0.0.0", port=port, debug=True)
