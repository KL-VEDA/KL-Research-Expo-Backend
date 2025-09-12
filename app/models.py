# app/models.py
from . import db
from werkzeug.security import generate_password_hash, check_password_hash

# -------------------------------
# USERS
# -------------------------------
class User(db.Model):
    __tablename__ = 'users'

    user_id = db.Column(db.String(64), primary_key=True)
    password_hash = db.Column(db.String(256), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


# -------------------------------
# TEAMS
# -------------------------------
class Team(db.Model):
    __tablename__ = 'teams'

    team_id = db.Column(db.Integer, primary_key=True)
    team_name = db.Column(db.String(255), unique=True, nullable=False)
    team_code = db.Column(db.String(64), unique=True)
    paper_drive_link = db.Column(db.Text, nullable=True)
    
    password = db.Column(db.Text, nullable=False)  # <-- New password column

    # Relationships
    members = db.relationship('Member', backref='team', cascade='all, delete-orphan')


# -------------------------------
# MEMBERS
# -------------------------------
class Member(db.Model):
    __tablename__ = 'members'

    member_id = db.Column(db.Integer, primary_key=True)
    team_id = db.Column(db.Integer, db.ForeignKey('teams.team_id'), nullable=False)
    
    name = db.Column(db.String(255), nullable=False)
    contact = db.Column(db.String(20))
    email = db.Column(db.String(255), unique=True, nullable=False)
    
    is_team_leader = db.Column(db.Boolean, default=False)

    # 🔍 Updated education details
    degree_program = db.Column(db.String(100), nullable=True)      # e.g., B.Tech, M.Tech, PhD, Faculty
    year_or_status = db.Column(db.String(100), nullable=True)      # e.g., 3rd Year, Completed, N/A
    institution = db.Column(db.String(255), nullable=True)         # e.g., KL University
    role = db.Column(db.String(100), nullable=True)                # e.g., Student, Faculty, Professor
