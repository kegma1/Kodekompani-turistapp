from __main__ import app, redirect, render_template, url_for, redirect, session
from flask import request
from db_utils import Attraction, db_session
from PIL import Image
from io import BytesIO
from base64 import b64encode
from libs.helpers import require_admin, require_login
from form.attraction_form import AttractionForm

@app.route("/admin_sights_edit_<id>", methods = ["GET", "POST"])
@require_login
@require_admin
def admin_sights_edit(id):
    attraction_form = AttractionForm()
    attraction = db_session.query(Attraction).filter_by(id = id).first()
    
    attraction_form.address.data = attraction.address
    attraction_form.age_recommendation.data = attraction.age_recommendation
    attraction_form.category.data = attraction.category
    attraction_form.description.data = attraction.description
    attraction_form.group.data = attraction.group
    attraction_form.image.data = attraction.image
    attraction_form.keywords.data = attraction.keywords
    attraction_form.location_coordinates.data = attraction.location_coordinates
    attraction_form.name.data = attraction.name
    
    return render_template("admin_sights_edit.html",
                           attraction = attraction_form,
                           image = attraction.image,
                           id = id,
                           title = "Admin sights edit")