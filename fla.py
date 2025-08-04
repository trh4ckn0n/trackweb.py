import sys
sys.path.insert(0, "/var/mobile/flask/src")

from flask import Flask, render_template_string, request
import subprocess
import os

app = Flask(__name__)

TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
  <title>trhacknon WebPanel</title>
  <style>
    body {
      background-color: black;
      color: lime;
      font-family: monospace;
      padding: 2rem;
    }
    input, button, textarea {
      background: #111;
      color: #0f0;
      border: 1px solid #0f0;
      padding: 5px;
      margin-top: 10px;
      width: 100%;
    }
  </style>
</head>
<body>
  <h1>📟 trhacknon Panel — iPhone</h1>

  <form method="post" action="/cmd">
    <label>💻 Commande shell :</label><br>
    <input name="cmd" placeholder="ex: ls /var/mobile" required>
    <button type="submit">Exécuter</button>
  </form>

  {% if output %}
    <h2>🔎 Résultat :</h2>
    <textarea rows="15">{{ output }}</textarea>
  {% endif %}
</body>
</html>
"""

@app.route("/", methods=["GET"])
def index():
    return render_template_string(TEMPLATE)

@app.route("/cmd", methods=["POST"])
def cmd():
    command = request.form.get("cmd")
    try:
        output = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT).decode()
    except subprocess.CalledProcessError as e:
        output = e.output.decode()
    return render_template_string(TEMPLATE, output=output)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
