import os
from flask import Flask
from client import f
app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello from Python!"

@app.route("/droplet")
def droplet():
    return f.droplet().toString()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
