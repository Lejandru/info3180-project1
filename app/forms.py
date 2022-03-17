from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from flask import Flask
from werkzeug.utils import secure_filename
from wtforms import StringField, SelectField, validators
from wtforms.validators import DataRequired

class PropertyForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    bedrooms = StringField('Bedrooms', validators=[DataRequired()])
    bathrooms = StringField('Bathrooms', validators=[DataRequired()])
    location = StringField('Location', validators=[DataRequired()])
    price = StringField('Price', validators=[DataRequired()])
    prop_type = SelectField('Type', choices=[('House'), ('Apartment')])
    description = StringField('Description', validators=[DataRequired()])
    imageFile = FileField('Photo', validators=[FileRequired(), FileAllowed(['jpg', 'png', 'jpeg'], 'Appropriate Images Only')])