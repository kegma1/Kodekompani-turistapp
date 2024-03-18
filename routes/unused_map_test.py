from __main__ import app
from flask import render_template, request

@app.route('/map_test')
def map_test():
    lat = 68.0
    lon = 17.0
    zoom = 4
    if request.args.get('lon'):
        lon = float(request.args.get('lon'))
    if request.args.get('lat'):
        lat = float(request.args.get('lat'))
    if request.args.get('zoom'):
        zoom = float(request.args.get('zoom'))
    return render_template("map_test.html", lon = lon, 
                           lat = lat, 
                           zoom = zoom)