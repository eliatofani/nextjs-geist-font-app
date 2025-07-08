from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField, FloatField, TextAreaField, SelectField, DateField, FileField
from wtforms.validators import DataRequired, Email, EqualTo, Length, NumberRange, Optional

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class RegisterForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

class WineForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    year = IntegerField('Year', validators=[Optional(), NumberRange(min=1900, max=2100)])
    type = StringField('Type', validators=[Optional()])
    region = StringField('Region', validators=[Optional()])
    alcohol = FloatField('Alcohol %', validators=[Optional(), NumberRange(min=0, max=100)])
    price = FloatField('Price', validators=[Optional(), NumberRange(min=0)])
    producer = StringField('Producer', validators=[Optional()])
    submit = SubmitField('Save')

class TastingForm(FlaskForm):
    wine_id = SelectField('Wine', coerce=int, validators=[DataRequired()])
    tasting_date = DateField('Tasting Date', validators=[DataRequired()])
    location = StringField('Location', validators=[Optional()])
    description = TextAreaField('Description', validators=[Optional()])
    submit = SubmitField('Save')

class VisualAnalysisForm(FlaskForm):
    color = SelectField('Color', choices=[('red', 'Red'), ('white', 'White'), ('rose', 'Rosé')], validators=[Optional()])
    color_density = SelectField('Color Density', choices=[('light', 'Light'), ('medium', 'Medium'), ('deep', 'Deep')], validators=[Optional()])
    clarity = SelectField('Clarity', choices=[('clear', 'Clear'), ('hazy', 'Hazy')], validators=[Optional()])
    consistency = SelectField('Consistency', choices=[('thin', 'Thin'), ('medium', 'Medium'), ('thick', 'Thick')], validators=[Optional()])
    bubble_size = SelectField('Bubble Size', choices=[('small', 'Small'), ('medium', 'Medium'), ('large', 'Large')], validators=[Optional()])
    bubble_number = SelectField('Bubble Number', choices=[('few', 'Few'), ('moderate', 'Moderate'), ('many', 'Many')], validators=[Optional()])
    bubble_persistence = SelectField('Bubble Persistence', choices=[('short', 'Short'), ('medium', 'Medium'), ('long', 'Long')], validators=[Optional()])
    submit = SubmitField('Save')

class OlfactoryAnalysisForm(FlaskForm):
    intensity = SelectField('Intensity', choices=[('low', 'Low'), ('medium', 'Medium'), ('high', 'High')], validators=[Optional()])
    complexity = SelectField('Complexity', choices=[('simple', 'Simple'), ('moderate', 'Moderate'), ('complex', 'Complex')], validators=[Optional()])
    quality = SelectField('Quality', choices=[('poor', 'Poor'), ('average', 'Average'), ('excellent', 'Excellent')], validators=[Optional()])
    dominant_aromas = StringField('Dominant Aromas', validators=[Optional()])
    submit = SubmitField('Save')

class GustatoryAnalysisForm(FlaskForm):
    sugar = SelectField('Sugar', choices=[('low', 'Low'), ('medium', 'Medium'), ('high', 'High')], validators=[Optional()])
    alcohol = SelectField('Alcohol', choices=[('low', 'Low'), ('medium', 'Medium'), ('high', 'High')], validators=[Optional()])
    acidity = SelectField('Acidity', choices=[('low', 'Low'), ('medium', 'Medium'), ('high', 'High')], validators=[Optional()])
    tannin_qty = SelectField('Tannin Quantity', choices=[('low', 'Low'), ('medium', 'Medium'), ('high', 'High')], validators=[Optional()])
    tannin_quality = SelectField('Tannin Quality', choices=[('poor', 'Poor'), ('average', 'Average'), ('excellent', 'Excellent')], validators=[Optional()])
    balance = SelectField('Balance', choices=[('poor', 'Poor'), ('average', 'Average'), ('excellent', 'Excellent')], validators=[Optional()])
    body = SelectField('Body', choices=[('light', 'Light'), ('medium', 'Medium'), ('full', 'Full')], validators=[Optional()])
    persistence = SelectField('Persistence', choices=[('short', 'Short'), ('medium', 'Medium'), ('long', 'Long')], validators=[Optional()])
    quality = SelectField('Quality', choices=[('poor', 'Poor'), ('average', 'Average'), ('excellent', 'Excellent')], validators=[Optional()])
    submit = SubmitField('Save')

class UploadForm(FlaskForm):
    file = FileField('Upload Image', validators=[DataRequired()])
    submit = SubmitField('Upload')
