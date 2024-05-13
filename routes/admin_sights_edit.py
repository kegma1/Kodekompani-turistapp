from __main__ import app
from flask import request, redirect, render_template, url_for, redirect
from db_utils import Attraction, db_session
from libs.helpers import require_local_admin, require_login
from form.attraction_form import AttractionForm
from werkzeug.datastructures import CombinedMultiDict

@app.route("/admin_sights_edit_<attraction_id>", methods = ["GET", "POST"])
@require_login
@require_local_admin
def admin_sights_edit(attraction_id):
    attraction_form = AttractionForm(data_required=False, formdata=CombinedMultiDict((request.files, request.form)))
    attraction = db_session.query(Attraction).filter_by(id = attraction_id).first()
    
    if request.method == "POST" and attraction_form.validate():
        attraction.address = attraction_form.address.data
        attraction.age_recommendation = attraction_form.age_recommendation.data
        attraction.category = attraction_form.category.data
        attraction.description = attraction_form.description.data
        attraction.group = attraction_form.group.data
        attraction.isDeleted = attraction_form.isDeleted.data
        
        if attraction_form.image.data:
            attraction.image = attraction_form.image.data
            
        attraction.keywords = attraction_form.keywords.data
        attraction.location_coordinates = attraction_form.location_coordinates.data
        attraction.name = attraction_form.name.data
        attraction.local_admin_id = attraction_form.local_admin.data
        
        db_session.commit()
        
        return redirect(url_for("admin_sights", page = 1))
    
    attraction_form.address.data = attraction.address
    attraction_form.age_recommendation.data = attraction.age_recommendation
    attraction_form.category.data = attraction.category
    attraction_form.description.data = attraction.description
    attraction_form.group.data = attraction.group
    attraction_form.isDeleted.data = attraction.isDeleted
    attraction_form.keywords.data = attraction.keywords
    attraction_form.location_coordinates.data = attraction.location_coordinates
    attraction_form.name.data = attraction.name
    attraction_form.local_admin.data = attraction.local_admin_id

    lat, lon  = attraction.location_coordinates.split(",")
    
    return render_template("admin_sights_edit.html",
                           attraction = attraction_form,
                           image = attraction.image,
                           id = attraction_id,
                           title = "Admin sights edit",
                           lon=lon,
                           lat=lat)