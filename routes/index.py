from __main__ import app, render_template

@app.route("/", methods = ["GET"])
def index():
    return render_template("index.html")