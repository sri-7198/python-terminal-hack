from flask import Flask, request, jsonify
import subprocess, os, psutil

app = Flask(__name__)

# Run system shell commands (ls, pwd, mkdir, rm, etc.)
@app.route("/terminal", methods=["POST"])
def terminal():
    data = request.get_json(silent=True) or {}
    cmd = data.get("command", "")

    if not cmd.strip():
        return jsonify({"error": "No command provided"}), 400

    try:
        output = subprocess.check_output(
            cmd, shell=True, stderr=subprocess.STDOUT, timeout=5
        )
        return jsonify({"stdout": output.decode(), "stderr": "", "returncode": 0})
    except subprocess.CalledProcessError as e:
        return jsonify({
            "stdout": e.output.decode(),
            "stderr": str(e),
            "returncode": e.returncode
        })
    except Exception as ex:
        return jsonify({"stdout": "", "stderr": str(ex), "returncode": 1})


# Run Python snippets
@app.route("/local_run", methods=["POST"])
def local_run():
    data = request.get_json(silent=True) or {}
    code = data.get("code", "")

    if not code.strip():
        return jsonify({"error": "No Python code provided"}), 400

    fname = "/tmp/snippet.py"
    try:
        with open(fname, "w") as f:
            f.write(code)

        proc = subprocess.run(
            ["python3", fname],
            capture_output=True,
            text=True,
            timeout=5
        )
        return jsonify({
            "stdout": proc.stdout,
            "stderr": proc.stderr,
            "returncode": proc.returncode
        })
    except subprocess.TimeoutExpired:
        return jsonify({"stdout": "", "stderr": "Timeout (5s)", "returncode": 124})
    except Exception as e:
        return jsonify({"stdout": "", "stderr": str(e), "returncode": 1})
    finally:
        try:
            os.remove(fname)
        except:
            pass


# System monitoring (CPU, memory, processes)
@app.route("/sysinfo", methods=["GET"])
def sysinfo():
    return jsonify({
        "cpu_percent": psutil.cpu_percent(),
        "memory_percent": psutil.virtual_memory().percent,
        "process_count": len(psutil.pids())
    })


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5001))
    app.run(host="0.0.0.0", port=port, debug=True)
