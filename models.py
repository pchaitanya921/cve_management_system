from flask_sqlalchemy import SQLAlchemy
from models import CVEEntry


db = SQLAlchemy()
class CVEEntry:
    def __init__(self, cve_id, description, published_date, severity):
        self.cve_id = cve_id
        self.description = description
        self.published_date = published_date
        self.severity = severity

    def to_dict(self):
        return {
            "cve_id": self.cve_id,
            "description": self.description,
            "published_date": self.published_date,
            "severity": self.severity,
        }


class CVE(db.Model):
    __tablename__ = 'cves'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    cve_id = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.Text, nullable=False)
    severity = db.Column(db.String(20), nullable=False)
    published_date = db.Column(db.DateTime, nullable=False)
    last_modified_date = db.Column(db.DateTime, nullable=True)

    def __repr__(self):
        return f"<CVE {self.cve_id}>"

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    role = db.Column(db.String(20), default="user")  # admin/user

    def __repr__(self):
        return f"<User {self.username}>"

class CVELog(db.Model):
    __tablename__ = 'cve_logs'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    cve_id = db.Column(db.String(50), nullable=False)
    action = db.Column(db.String(50), nullable=False)  # e.g., 'viewed', 'reported'
    timestamp = db.Column(db.DateTime, default=db.func.current_timestamp())

    user = db.relationship('User', backref=db.backref('logs', lazy=True))

    def __repr__(self):
        return f"<CVELog {self.user_id} {self.cve_id} {self.action}>"

def init_db(app):
    """ Initialize the database with the Flask app """
    db.init_app(app)
    with app.app_context():
        db.create_all()
