import datetime

from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
db =SQLAlchemy(app)


class Project(db.Model):
    id = db.Column(db.integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(100), nullable=False)
    link = db.Column(db.String(100), nullable=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
    finished = db.Column(db.Boolean)

    def __repr__(self):
        return f'<Project {self.title}>'


@app.route("/")
def hello_world():
    return render_template("index.html")
