import os
import json
from flask import Flask
from client import f
app = Flask(__name__)

@app.route("/")
def hello():
    return "ELE 201 project on Fountain Codes by David Bieber."

@app.route("/droplet")
def droplet():
    return f.droplet().toString()

@app.route("/droplet/<amt>")
def droplets(amt):
    out = []
	for x in xrange(amt):
		out.append(f.droplet().toString())
	return json.dumps(out)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
