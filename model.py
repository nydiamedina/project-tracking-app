import datetime
import os

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):

    __tablename__ = "users"

    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    first_name = db.Column(db.String(255), nullable=True)
    last_name = db.Column(db.String(255), nullable=True)
    created_at = db.Column(
        db.DateTime, nullable=False, default=datetime.datetime.utcnow
    )
    updated_at = db.Column(
        db.DateTime, nullable=False, default=datetime.datetime.utcnow
    )

    teams = db.relationship("Team", backref="user", lazy=True)

    def __init__(self, username, password, **kwargs):
        self.username = username
        self.password = password

        if "first_name" in kwargs:
            self.first_name = kwargs["first_name"]

        if "last_name" in kwargs:
            self.last_name = kwargs["last_name"]


class Team(db.Model):

    __tablename__ = "teams"

    team_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    team_name = db.Column(db.String(255), unique=True, nullable=False)
    team_description = db.Column(db.String(255), unique=True, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), nullable=False)
    created_at = db.Column(
        db.DateTime, nullable=False, default=datetime.datetime.utcnow
    )
    updated_at = db.Column(
        db.DateTime, nullable=False, default=datetime.datetime.utcnow
    )

    projects = db.relationship("Project", backref="team", lazy=True)

    def __init__(self, team_name, user_id, **kwargs):
        self.team_name = team_name
        self.user_id = user_id

        if "team_description" in kwargs:
            self.last_name = kwargs["team_description"]


class Project(db.Model):

    __tablename__ = "projects"

    project_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    project_name = db.Column(db.String(255), nullable=False)
    project_description = db.Column(db.String(255), nullable=True)
    is_completed = db.Column(db.Boolean, default=False)
    team_id = db.Column(db.Integer, db.ForeignKey("teams.team_id"), nullable=False)
    created_at = db.Column(
        db.DateTime, nullable=False, default=datetime.datetime.utcnow
    )
    updated_at = db.Column(
        db.DateTime, nullable=False, default=datetime.datetime.utcnow
    )

    def __init__(self, project_name, is_completed, team_id, **kwargs):
        self.project_name = project_name
        self.is_completed = is_completed
        self.team_id = team_id

        if "project_description" in kwargs:
            self.project_description = kwargs["project_description"]


def connect_to_db(app):
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ["POSTGRES_URI"]
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    from flask import Flask

    app = Flask(__name__)
    connect_to_db(app)
    print("Connected to db...")
