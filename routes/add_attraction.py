from __main__ import app
from libs.helpers import require_admin, require_login
from flask import redirect, render_template, url_for, request
from db_utils import db_session, Attraction
from form.attraction_form import AttractionForm
from werkzeug.datastructures import CombinedMultiDict

@app.route("/add_attraction", methods=["GET", "POST"])
@require_login
@require_admin
def add_attraction():
    attraction_form = AttractionForm(data_required=True, formdata=CombinedMultiDict((request.files, request.form)))
    if request.method == "POST" and attraction_form.validate_on_submit():
        new_attraction = Attraction()

        new_attraction.name = attraction_form.name.data
        new_attraction.description = attraction_form.description.data
        new_attraction.category = attraction_form.category.data
        new_attraction.age_recommendation = attraction_form.age_recommendation.data
        new_attraction.location_coordinates = attraction_form.location_coordinates.data
        new_attraction.address = attraction_form.address.data
        new_attraction.group = attraction_form.group.data
        new_attraction.keywords = attraction_form.keywords.data
        new_attraction.image = attraction_form.image.data.stream
        new_attraction.local_admin_id = attraction_form.local_admin.data

        db_session.add(new_attraction)
        db_session.commit()
        return redirect(url_for("admin_sights", page = 1))
        
    return render_template("admin_add_attraction.html", title="Add attraction", form=attraction_form)
