from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField, BooleanField
from wtforms.validators import DataRequired, Length

class UserForm(FlaskForm):
    username = StringField("Username: ", validators=[DataRequired()])
    password = PasswordField("Password: ", validators=[DataRequired()])
    fname = StringField("First name: ", validators=[DataRequired()])
    submit = SubmitField("Register")

class LoginForm(FlaskForm):
    username = StringField("Username: ", validators=[DataRequired()])
    password = PasswordField("Password: ", validators=[DataRequired()])
    remember_me = BooleanField("Keep me logged in")
    submit = SubmitField("Log In")

class DeleteForm(FlaskForm):
    username = StringField("Enter the username to remove: ", validators=[DataRequired()])
    submit = SubmitField("Delete User")
    
class AddForm(FlaskForm):
    post = StringField("What do you want to let people know? ", validators=[DataRequired()])
    submit = SubmitField("Post!")

# class SearchForm(FlaskForm):
#     item = StringField("Need to look up an item? ", validators=[DataRequired()], render_kw={"placeholder": "look up a product name"})
#     submit = SubmitField("Search")
    
class USearchForm(FlaskForm):
    fname = StringField("Search for a user: ", validators=[DataRequired()], render_kw={"placeholder": "search by username"})
    submit = SubmitField("Search")


# class ItemForm(FlaskForm):
#     name = StringField("Enter the name of the item: ", validators=[DataRequired()])
#     price = IntegerField("Enter the price of the item: ", validators=[DataRequired()])
#     quantity = IntegerField("Enter how many are being sold: ", validators=[DataRequired()])
#     submit = SubmitField("Add Item")

# class DItemForm(FlaskForm):
#     name = StringField("Enter the name of the item to delete: ", validators=[DataRequired()])
#     submit = SubmitField("Remove Item")

# class LikeItem(FlaskForm):
#     username = StringField("Enter the username to reserve under: ", validators=[DataRequired()])
#     name = StringField("Enter the product to put on hold: ", validators=[DataRequired()])
#     submit = SubmitField("Put On Hold")