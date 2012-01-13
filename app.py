import os
import json
from flask import Flask, render_template, redirect
from client import f
from glass import Glass
import random
app = Flask(__name__)

glasses = {}

@app.route("/")
def home():
    return render_template('home.html')

@app.route("/droplet")
def droplet():
    return f.droplet().toString()

@app.route("/droplet/<amt>")
def droplets(amt):
    amt = int(amt)
    out = []
    for x in range(amt):
        out.append(f.droplet().toString())
    return json.dumps(out)
    
@app.route("/glass")
def pickGlass():
    return redirect("/glass/%d" % random.randint(0,2**15-1))

@app.route("/glass/<id>")
def glass(id):
    id = int(id)
    g = getGlass(id)
    message = "%d of %d chunks reconstructed." % (g.chunksDone(), g.num_chunks)
    
    return render_template('glass.html',
        num_droplets=len(g.droplets),
        source="/droplet",
        text=g.getString(),
        id=id,
        droplets=[d for d in g.droplets],
        message=message
        )
     
@app.route("/glass/<id>/fill")
def fill(id):
    return fillAmt(id, 1)
    
@app.route("/glass/<id>/fill/<amt>")
def fillAmt(id, amt):
    id = int(id)
    amt = int(amt)
    
    g = getGlass(id)
    for i in xrange(amt):
        g.addDroplet(f.droplet())
    return redirect("/glass/%d" % id)
        
def getGlass(id):
    id = int(id)
    g = None
    if id not in glasses:
        g = Glass(f.num_chunks) 
        glasses[id] = g
    return glasses[id]

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
