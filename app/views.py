"""
Flask Documentation:     https://flask.palletsprojects.com/
Jinja2 Documentation:    https://jinja.palletsprojects.com/
Werkzeug Documentation:  https://werkzeug.palletsprojects.com/
This file creates your application.
"""

import os
from app import app
from flask import render_template, request, redirect, url_for, flash, send_from_directory
from app.forms import PropertyForm
from werkzeug.utils import secure_filename
from app import db
from app.models import UserProperty


###
# Routing for your application.
###

@app.route('/')
def home():
    """Render website's home page."""
    return render_template('home.html')


@app.route('/about/')
def about():
    """Render the website's about page."""
    return render_template('about.html', name="Lejandru Richards")

@app.route('/property', methods = ['POST', 'GET'])
def property():
    myform = PropertyForm()

    if request.method == 'POST':
        if myform.validate_on_submit():
            title = myform.title.data
            bedrooms = myform.bedrooms.data
            bathrooms = myform.bathrooms.data
            location = myform.location.data
            price = myform.price.data
            prop_type = myform.prop_type.data
            description = myform.description.data
            image = myform.imageFile.data

            filename = secure_filename(image.filename)
            image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            property = UserProperty(title, bedrooms, bathrooms, location, price, prop_type, description, filename)
            db.session.add(property)
            db.session.commit()

            flash('You have successfully uploaded a property')
            return redirect(url_for('properties'))
    return render_template('property.html', form=myform)


@app.route('/properties')
def properties():
    properties = UserProperty.query.all()
    return render_template('properties.html', properties=properties)


@app.route('/property/<propertyid>')
def propertyById(propertyid):
    properties = db.session.query(UserProperty).filter(UserProperty.id == propertyid).first()
    return render_template('propertyById.html', properties=properties)


@app.route('/uploads/<filename>')
def get_image(filename):
    root_dir = os.getcwd()
    return send_from_directory(os.path.join(root_dir, app.config['UPLOAD_FOLDER']), filename)


def get_uploaded_images():
    rootdir = os.getcwd()
    images = []
    for subdir, dirs, files in os.walk(rootdir + '/uploads'):
        for file in files:
            ##image_path = os.path.join(subdir, file)
            images.append(file)
    images.pop[0]
    return images
    
###
# The functions below should be applicable to all Flask apps.
###

# Display Flask WTF errors as Flash messages
def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Error in the %s field - %s" % (
                getattr(form, field).label.text,
                error
            ), 'danger')

@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also tell the browser not to cache the rendered page. If we wanted
    to we could change max-age to 600 seconds which would be 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(debug=True,host="0.0.0.0",port="8080")
