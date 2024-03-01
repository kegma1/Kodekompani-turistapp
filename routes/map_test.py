from __main__ import app
from flask import render_template

@app.route('/map_test')
def map_test():
    return render_template("map_test.html", title="TEST")