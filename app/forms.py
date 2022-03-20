from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from flask import Flask
from werkzeug.utils import secure_filename
from wtforms import StringField, SelectField, validators
from wtforms.validators import DataRequired

class PropertyForm(FlaskForm):
    title = StringField('Property Title', validators=[DataRequired()])
    description = StringField('Description', validators=[DataRequired()])
    bedrooms = StringField('No. of Rooms', validators=[DataRequired()])
    bathrooms = StringField('No. of Bathrooms', validators=[DataRequired()])
    price = StringField('Price', validators=[DataRequired()])
    prop_type = SelectField('Property Type', choices=[('House'), ('Apartment')])
    location = StringField('Location', validators=[DataRequired()])
    imageFile = FileField('Photo', validators=[FileRequired(), FileAllowed(['jpg', 'png', 'jpeg'], 'Appropriate Images Only')])