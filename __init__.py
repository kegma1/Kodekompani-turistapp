from flask import Flask
import secrets


app = Flask(__name__)

app.secret_key = secrets.token_urlsafe(16)

@app.route("/", methods = ["GET"])
def index():
    return "Hallo, Verden!"

if __name__ == "__main__":
    app.run()