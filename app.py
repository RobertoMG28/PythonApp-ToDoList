from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy



app = Flask(__name__, template_folder='templates')
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

class Tarea(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(100))
    complete = db.Column(db.Boolean)



@app.route('/')
def index():
    #Mostrar Tareas

    lista_tareas = Tarea.query.all()
    #print(lista_tareas)
    #print(lista_tareas[0], lista_tareas[1])

    return render_template("base.html", todo_list = lista_tareas)


@app.route("/add", methods =["POST"])   
def add():
    #Añadir Nueva Tarea
    title = request.form.get("title")
    if title == "":
        return redirect(url_for("index"))
    else:
        nueva_tarea = Tarea(title=title, complete=False)
        db.session.add(nueva_tarea)
        db.session.commit()
        return redirect(url_for("index"))

@app.route("/update/<int:tarea_id>")   
def update(tarea_id):
    #Actualizar Tareas
    tarea = Tarea.query.filter_by(id=tarea_id).first()
    tarea.complete = not tarea.complete
    db.session.commit()
    return redirect(url_for("index"))

@app.route("/delete/<int:tarea_id>")   
def delete(tarea_id):
    #Actualizar Tareas
    tarea = Tarea.query.filter_by(id=tarea_id).first()
    db.session.delete(tarea)
    db.session.commit()
    return redirect(url_for("index"))



if __name__ == "__main__":
    db.create_all()
    app.run(debug = True)
    