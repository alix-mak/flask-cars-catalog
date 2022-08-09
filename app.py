from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cars.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Car(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    description = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __str__(self):
        return self.name

    def __repr__(self):
        return '<Car %r>' % self.id


@app.route('/home/')
@app.route('/')
def index():
    cars = Car.query.order_by(Car.name).all()
    return render_template("index.html", cars=cars)


@app.route('/about/')
def about():
    return render_template("about.html")


@app.route('/create-car/', methods=['POST', 'GET'])
def create_car():
    if request.method == "POST":
        name = request.form['name']
        description = request.form['description']

        car = Car(name=name, description=description)

        try:
            db.session.add(car)
            db.session.commit()
            return redirect('/articles/')

        except:
            return "An error occurred when adding a new car"

    else:
        return render_template("create-car.html")


@app.route('/articles/')
def articles():
    cars = Car.query.order_by(Car.name).all()
    return render_template("articles.html", cars=cars)


@app.route('/articles/<int:id>/update/', methods=['POST', 'GET'])
def car_update(id):
    car = Car.query.get(id)
    if request.method == "POST":
        car.name = request.form['name']
        car.description = request.form['description']

        try:
            db.session.commit()
            return redirect('/articles/')

        except:
            return "An error occurred when editing a car"

    else:
        car = Car.query.get(id)
        return render_template("car-update.html", car=car)


@app.route('/articles/<int:id>')
def article_detail(id):
    car = Car.query.get(id)
    return render_template("article_detail.html", car=car)


@app.route('/articles/<int:id>/delete')
def article_delete(id):
    car = Car.query.get_or_404(id)

    try:
        db.session.delete(car)
        db.session.commit()
        return redirect('/articles/')
    except:
        return "An error occurred when deleting a new car"


if __name__ == '__main__':
    app.run(debug=True)
