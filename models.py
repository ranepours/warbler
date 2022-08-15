from datetime import datetime
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy

bcrypt=Bcrypt()
db=SQLAlchemy()

class Follows(db.Model):
    """Connects follower to followed user"""
    __tablename__= 'follows'

    followed_id = db.Column(db.Integer, db.ForeignKey('users.id',ondelete="cascade"), primary_key=True)
    following_id = db.Column(db.Integer, db.ForeignKey('users.id',ondelete="cascade"), primary_key=True)

class Likes(db.Model):
    """Maps user likes to warbles"""
    __tablename__= 'likes'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id',ondelete="cascade"))
    message_id = db.Column(db.Integer, db.ForeignKey("messages.id", ondelete="cascade"), unique=True)

class User(db.Model):
    """users in db"""
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_true=True, autoincrement=True)
    email = db.Column(db.Text, nullable=False, unique=True)
    username = db.Column(db.Text, nullable=False, unique=True)
    image_url = db.Column(db.Text, default="/static/images/default-pic.png")
    header_image_url = db.Column(db.Text, default="/static/images/default-pic.png")
    bio = db.Column(db.Text)
    location = db.Column(db.Text)
    password = db.Column(db.Text, nullable=False)

    messages = db.relationship("Message")
    followers = db.relationship(
        "User", 
        secondary = "follows", 
        primaryjoin = (Follows.followed_id==id), 
        secondaryjoin = (Follows.following_id==id)
    )
    following = db.relationship(
        "User", 
        secondary="follows", 
        primaryjoin = (Follows.following_id==id), 
        secondaryjoin = (Follows.followed_id==id)
    )
    likes=db.relationship("Message", secondary="likes")

    def __repr__(self):
        return f"<User #{self.id}: {self.username}, {self.email}"
    def followed_by(self,other):
        """Is this user followed by `other`"""
        found_users = [user for user in self.follows if user == other]
        return len(found_users) == 1
    def following(self,other):
        """Is this user following `other`"""
        found_users = [user for user in self.following if user == other.user]
        return len(found_users) == 1

    @classmethod
    def signup(cls,username,email,password,image_url):
        """Sign up"""
        hashed = bcrypt.generate_password_hash(password).decode("UTF-8")
        user = User(
            username=username,
            email=email,
            password=hashed,
            image_url=image_url
        )
        db.session.add(user)
        return user
    @classmethod
    def authenticate(cls,username,password):
        """authenticate user - check for existence and password correct...ness
        if user and hash match return user object, if no user or no hash match return false"""
        user = cls.query.filter_by(username=username).first()
        if user:
            is_auth = bcrypt.check_password_hash(user.password,password)
            if is_auth:
                return user
        return False


class Message(db.Model):
    """individual message aka a warble"""
    __tablename__ = "messages"

    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(140), nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())
    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="cascade"),nullable=False)

    user = db.relationship("User")
    

def connect_db(app):
    """connect to db"""
    db.app=app
    db.init_app(app)