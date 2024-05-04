from __main__ import app
from flask import url_for, send_file
import qrcode
from io import BytesIO

@app.route('/qr/<attraction_id>/<passcode>', methods=["GET"])
def qr_code(attraction_id: int, passcode: str):
    url = url_for("unlock_achivement", attraction = attraction_id, passcode = passcode, _external=True)
    qr_code = qrcode.make(url)

    qr_code_stream = BytesIO()
    qr_code.save(qr_code_stream, "PNG")
    qr_code_stream.seek(0)

    return send_file(qr_code_stream, mimetype="image/png")