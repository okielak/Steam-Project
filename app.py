import requests
from datetime import datetime
from flask import Flask, rain_info, redirect,  render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
db =SQLAlchemy(app)


class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(100), nullable=False)
    link = db.Column(db.String(100), nullable=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
    finished = db.Column(db.Boolean)

    def __repr__(self):
        return f'<Project {self.title}>'


@app.route("/")
def home():
    projects = Project.query.all()
    weather_data = get_weather_data()

    return render_template(
        "index.html",
        projects_list=projects,
        weather_data=weather_data,
    )


def get_weather_mood():
    weather_data = get_weather_data()

    temperature = float(weather_data['temperatura'])
    pressure = float(weather_data['ciśnienie'])
    rainfall = float(weather_data['suma_opadu'])

    pressure = 1013
    rainfall = 20

    if rainfall < 1:
        rain_info = 'Dziś nie pada :)'
    elif rainfall < 10:
        rain_info = 'Może lekko padać'
    else:
        rain_info = 'Weź parasol'


    if pressure <1010 or pressure> 1025:
        work_mood = 'mie sprzyja'
        comment='więc czekam na lepsze ciśnienie'
    else: #ciśnienie jest ok
        if rainfall <10: #nie pada
            if temperature > 20: #nie pada i jest ciepło
                work_mood = 'nie sprzyja'
                comment = 'nie pada więc możliwe, że jesteś offline'
            else: #nie pada i jest zimno
                work_mood = 'nie sprzyja'
                comment = 'nie pada więc możliwe, że jesteś offline'
        else: #pada
            work_mood = 'sprzyja'
            comment = 'więc prawdopodobnie pracuję nad, którymś z projektów'
        

    return f'Pogoda {work_mood} programowaniu, {comment}. PS {rain_info}'

def get_weather_data():
    url = 'https://danepubliczne.imgw.pl/api/data/synop/station/warszawa'
    response = requests.get(url)
    return response.json()

# żądanie wyświetl mi stronę główną - request HTTP GET /
# żądanie wyświetl mi szczegóły zadania - request HTTP GET /task/{id}
# żądanie wyświetl mi stronę z wszystkimi zadaniami - request HTTP GET /tasks
# żądanie utwórz nowe zadanie - request HTTP POST /task + dane


@app.route("/projects", methods=["POST"])
def add_project():
    title = request.form.get("title")
    category = request.form.get("category")
    link = request.form.get("link")

    new_project = Project(
        title=title,
        category=category,
        link=link
    )

    db.session.add(new_project)
    db.session.commit()
    db.session.close()
    return redirect(url_for('home'))

@app.route("/projects/<int:id>/delete")
def delete_project(id):
    project_to_delete = Project.query.get_or_404(id)

    db.session.delete(project_to_delete)
    db.session.commit()
    db.session.close()
    return redirect(url_for('home'))


@app.route("/projects/<int:id>/change_status")
def change_status(id):
    project = Project.query.get_or_404(id)

    project.finished = not project.finished
    db.session.commit()
    return redirect(url_for('home'))