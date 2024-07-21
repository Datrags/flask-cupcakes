"""Flask app for Cupcakes"""
from flask import Flask, jsonify, render_template, request
from models import Cupcake, db, connect_db

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "secret"

with app.app_context():
    connect_db(app)
    db.create_all()

# API ROUTES
@app.route("/api/cupcakes")
def get_cupcakes():
    cupcakes = [c.serialize() for c in Cupcake.query.all()]

    return jsonify(cupcakes=cupcakes)

@app.route("/api/cupcakes/<int:id>")
def get_cupcake(id):
    cupcake = Cupcake.query.get_or_404(id).serialize()

    return jsonify(cupcake=cupcake)

@app.route("/api/cupcakes", methods=["POST"])
def make_cupcake():
    cupcake = Cupcake(flavor=request.json["flavor"],
                      size=request.json["size"],
                      rating=request.json["rating"],
                      image=request.json["image"]
                      )
    db.session.add(cupcake)
    db.session.commit()

    return (jsonify(cupcake=cupcake.serialize()),201)

@app.route("/api/cupcakes/<int:id>", methods=["PATCH"])
def update_cupcake(id):
    cupcake = Cupcake.query.get_or_404(id)
    cupcake.flavor = request.json["flavor"]
    cupcake.size = request.json["size"],
    cupcake.rating = request.json["rating"],
    cupcake.image = request.json["image"]
    
    db.session.commit()

    return jsonify(cupcake=cupcake.serialize())

@app.route("/api/cupcakes/<int:id>", methods=["DELETE"])
def delete_cupcake(id):
    cupcake = Cupcake.query.get_or_404(id)
    db.session.delete(cupcake)
    db.session.commit()

    return jsonify(message="Deleted")

#VIEW ROUTES
@app.route("/")
def home_page():
    return render_template("home.html")