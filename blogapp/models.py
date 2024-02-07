from datetime import datetime
from blogapp import db, bcrypt, ma, login_manager
from flask_login import UserMixin
import uuid
import re

@login_manager.user_loader
def load_user(username):
    return User.query.get(username)

class User(db.Model, UserMixin):
    __tablename__ = 'user'

    id = db.Column(db.String(36) , primary_key=True, default=str(uuid.uuid4()), unique=True, nullable=False)
    first_name = db.Column(db.String(255), nullable=False)
    last_name = db.Column(db.String(255), nullable=False)
    _password = db.Column('password', db.String(255), nullable=False)
    username = db.Column(db.String(255), unique=True, nullable=False)
    account_created = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    account_updated = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    def __init__(self, first_name, last_name, password, username):
        self.first_name = first_name
        self.last_name = last_name
        self.password = password
        if not self.is_valid_email(username):
            raise ValueError("Invalid email address")
        self.username = username

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, plaintext_password):
        self._password = bcrypt.generate_password_hash(plaintext_password).decode('utf-8')

    def check_password(self, plaintext_password):
        return bcrypt.check_password_hash(self._password, plaintext_password)

    def is_valid_email(self, email):
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
        return bool(re.match(email_pattern, email))

class UserSchema(ma.Schema):
    class Meta:
        fields = ('id', 'first_name', 'last_name', 'username', 'account_created', 'account_updated')

user_schema = UserSchema()
users_schema = UserSchema(many=True)
