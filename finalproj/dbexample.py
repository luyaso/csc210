import os
from flask import Flask, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from wtforms import PasswordField, IntegerField, BooleanField
from wtforms.validators import Length

basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(basedir, "data.sqlite")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = "lucyssupersecretkeyissupersecret"

db = SQLAlchemy(app)

class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key = True)
    firstname = db.Column(db.String(64), index = True)
    username = db.Column(db.String(64), unique = True, index = True)
    password_hash = db.Column(db.String(128))
    myposts = db.Column(db.String(200), db.ForeignKey("posts.id"))

    def __repr__(self):
        return "<user %r>" % self.username
    
    @property
    def password(self):
        raise AttributeError("password is not a readable attribute")
    
    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)
        
    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    
class Post(UserMixin, db.Model):
    __tablename__ = "posts"
    id = db.Column(db.Integer, primary_key = True)
    user = db.relationship("User", backref = "post")
    username = db.Column(db.String(64))
    summary = db.Column(db.String(200))

    def __repr__(self):
        return self.id

# @login_manager.user_loader
# def load_user(user_id):
#     return User.query.get(int(user_id))

# @app.route("/", methods = ["GET", "POST"])
# def index():

#     form = SearchForm()

#     if (form.validate_on_submit()):
#         item = form.item.data
#         products = Product.query.filter_by(name = item).all()
#         return render_template("mainpage.html", form = form, products = products, search = True, item = item)
#     else:
#         products = Product.query.all()
#         return render_template("mainpage.html", form = form, products = products, search = False)

@app.route("/", methods = ["GET", "POST"])
def index():
    return render_template("mainpage.html")


@app.route("/login", methods=["GET", "POST"])
def login():

    form = LoginForm()

    if (form.validate_on_submit()):
        user = User.query.filter_by(username = form.username.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            next = request.args.get("next")
            if next is None or not next.startswith("/"):
                next = url_for("main.index")
            return redirect(next)
        flash("Invalid username or password.")

    return render_template("login.html", form = form)

@app.route("/logout")
# @login_required
# def logout():
#     logout_user()
#     flash("You have been logged out.")
#     return redirect(url_for("main.index"))


@app.route("/add.html", methods = ["GET", "POST"])
def add():

    form = UserForm()
    
    if(form.validate_on_submit()):
        username = form.username.data
        if(User.query.filter_by(username).first() is None):
            fname = form.fname.data
            pw = form.password.data
            createUser(username, pw, fname)

            return redirect(url_for("main.index"))
        flash ("This username is already taken!")
        
    return render_template("add.html", form = form)

@app.route("/delete.html", methods = ["GET", "POST"])
def delete():

    form = DeleteForm()
    
    if(form.validate_on_submit()):
        username = form.username.data
        if (User.query.filter_by(username).first() is not None):
            deleteUser(username)
            return redirect(url_for("main.index"))
        flash ("No user with that name found.")
        
    return render_template("delete.html", form = form)



def createUser(username, password, fname):
    user = User(username = username, password = password, firstname = fname)
    db.session.add(user)
    db.session.commit()
    
def deleteUser(username):
    user = User.query.filter_by(username = username).first()
    if(user != None):
        db.session.delete(user)
        db.session.commit()

        
# def createItem(name, price, quantity):
#     product = Product(name = name, price = price, quantity = quantity)
#     db.session.add(product)
#     db.session.commit()

# def likedItem(username, item):
#     user = User.query.filter_by(username = username).first()
#     item = Product.query.filter_by(item = item).first()
#     if(user != None and product != None):
#         user.liked_item = item.id
#         db.session.commit()

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
    
# class SearchForm(FlaskForm):
#     item = StringField("Search for a product: ", validators=[DataRequired()])
#     submit = SubmitField("Search")
    