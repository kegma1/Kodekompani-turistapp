from flask import Flask, render_template
import secrets


app = Flask(__name__)

app.secret_key = secrets.token_urlsafe(16)

@app.route("/", methods = ["GET"])
def index():
    return render_template("index.html")

if __name__ == "__main__":
    app.run()