from flask import session, request
from flask import render_template, redirect, url_for, flash

from . import main
from .. import db

from ..models import User, Post
from .forms import UserForm, LoginForm, DeleteForm, USearchForm, AddForm

from flask_login import login_required, current_user
from flask_login import login_user, logout_user


rps = ["rock", "paper", "scissors"]
rpsimg = ["images/rock.png", "images/paper.png", "images/scissors.png"]

@main.route("/", methods = ["GET", "POST"])
def index():

    mylogin = False
    if current_user.is_authenticated:
        mylogin = True

    posts = Post.query.all()

    return render_template("mainpage.html", loggedin = mylogin, posts = posts)


@main.route("/login", methods=["GET", "POST"])
def login():

    form = LoginForm()

    if current_user.is_authenticated:
        return render_template("mainpage.html")

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

@main.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("main.index"))


@main.route("/myaccount.html", methods = ["GET", "POST"])
@login_required
def myacc():

    user = current_user
    
    return render_template("myaccount.html", user = user)


@main.route("/add.html", methods = ["GET", "POST"])
def add():

    form = UserForm()

    if current_user.is_authenticated:
        return render_template("mainpage.html")
    
    if(form.validate_on_submit()):
        username = form.username.data
        if(User.query.filter_by(username = username).first() is None):
            fname = form.fname.data
            pw = form.password.data
            createUser(username, pw, fname)

            return redirect(url_for("main.login"))
        flash("This username already exists!")
        
    return render_template("add.html", form = form)

@main.route("/delete.html", methods = ["GET", "POST"])
@login_required
def delete():

    form = DeleteForm()
    
    if(form.validate_on_submit()):
        username = form.username.data
        if (User.query.filter_by(username = username).first() is not None):
            deleteUser(username)
            return redirect(url_for("main.index"))
        flash("No user with that name found.")
        
    return render_template("delete.html", form = form)

@main.route("/usertable.html", methods = ["GET", "POST"])
def usersearch():
    
    form = USearchForm()
    
    if(form.validate_on_submit()):
        fname = form.fname.data
        users = User.query.filter_by(username = fname).first()
        posts = users.myposts
        return render_template("usertable.html", form = form, users = users, posts = posts, search = True, fname = fname)
    else:
        users = User.query.all()
        return render_template("usertable.html", form = form, users = users, search = False)
    
@main.route("/tac.html", methods = ["GET", "POST"])
def tacpage():
    return render_template("tac.html")    

@main.route("/user.html", methods = ["GET", "POST"])
@login_required
def userposts(user):

    if (User.query.filter_by(username = user).first() is not None):
        if (Post.query.filter_by(user = user).all() is not None):
            return render_template("user.html", grace = True, user = user, history = True, posts = Post.query.filter_by(user = user).all())
        return render_template("user.html", grace = True, user = user, history = False)

    flash("No such user!")
    return render_template("user.html", grace = False)

@main.route("/addpost.html", methods = ["GET", "POST"])
@login_required
def addpost():

    form = AddForm()

    if(form.validate_on_submit()):
        user = current_user
        summary = form.post.data

        createPost(user, summary)
        
        return redirect(url_for("main.index"))

    return render_template("addpost.html", form = form)
    


def createUser(username, password, fname):
    user = User(username = username, password = password, firstname = fname)
    db.session.add(user)
    db.session.commit()
    
def deleteUser(username):
    user = User.query.filter_by(username = username).first()
    db.session.delete(user)
    db.session.commit()

def createPost(user, summary):
    post = Post(summary = summary, username = user.username)
    db.session.add(post)
    user.myposts = post.id

    db.session.commit()