from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

from . import login_manager

class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key = True)
    firstname = db.Column(db.String(64), index = True)
    username = db.Column(db.String(64), unique = True, index = True)
    password_hash = db.Column(db.String(128))
    myposts = db.Column(db.String(200), db.ForeignKey("posts.id"))

    def __repr__(self):
        return "username: %r" % self.username
    
    @property
    def password(self):
        raise AttributeError("password is not a readable attribute")
    
    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)
        
    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

class Post(db.Model):
    __tablename__ = "posts"
    id = db.Column(db.Integer, primary_key = True)
    user = db.relationship("User", backref = "post")
    username = db.Column(db.String(64))
    summary = db.Column(db.String(200))

    def __repr__(self):
        return self.id


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))