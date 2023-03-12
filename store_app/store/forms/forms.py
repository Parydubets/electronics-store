""" The form  file """
from datetime import date
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateField, IntegerField
from wtforms.validators import DataRequired, Length, Email, NumberRange


year=date.today()
class CreateClientForm(FlaskForm):
    """ The client form """
    first_name  = StringField("First name", validators=[DataRequired(), Length(min=1, max=40)])
    last_name   = StringField("Last name", validators=[DataRequired(), Length(min=1, max=40)])
    email       = StringField("Email", validators=[DataRequired(), Email(), Length(min=6, max=80)])
    phone       = StringField("Phone", validators=[DataRequired(), Length(min=13, max=13)])
    cancel = SubmitField("Cancel")
    submit = SubmitField("Save")



class CreateOrderForm(FlaskForm):
    """ The order form """
    name        = StringField("Full name", validators=[DataRequired(), Length(min=6, max=80)])
    phone       = StringField("Phone", validators=[DataRequired(), Length(min=13, max=13)])
    order       = StringField("Order", validators=[DataRequired(), Length(min=5, max=200)])
    address     = StringField("Address", validators=[DataRequired(), Length(min=5, max=160)])
    date        = DateField("Date", validators=[DataRequired()])
    cancel = SubmitField("Cancel")
    submit = SubmitField("Save")


class CreateProductForm(FlaskForm):
    """ The product form """
    name        = StringField("Product name",\
                    validators=[DataRequired(), Length(min=6, max=40)])
    cost       = IntegerField("Price",\
                    validators=[DataRequired(), NumberRange(min=1, max=100000)])
    category    = StringField("Category",\
                    validators=[DataRequired(), Length(min=2, max=20)])
    year        = IntegerField("Year",\
                    validators=[DataRequired(), NumberRange(min=2000, max=2023)])
    amount      = IntegerField("Amount",\
                    validators=[DataRequired(), NumberRange(min=1, max=100000)])
    cancel = SubmitField("Cancel")
    submit = SubmitField("Save")


class Filters(FlaskForm):
    """ The filters form """
    date_from   = DateField("from:", validators=[DataRequired()])
    date_to     = DateField("to:", validators=[DataRequired()])
    price_from  = IntegerField("from:",  validators=[DataRequired()])
    price_to    = IntegerField("to:",  validators=[DataRequired()])
    refresh     = SubmitField("Filter")


class DeleteItem(FlaskForm):
    """ The dalete form """
    cancel = SubmitField("No")
    submit = SubmitField("Yes")
