from flask import Flask
import os

app = Flask(__name__)
PORT = int(os.environ.get("FLASK_PORT", 5000))

@app.route("/")
def hello():
    return f"Hello from Flask running on port {PORT}"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT)