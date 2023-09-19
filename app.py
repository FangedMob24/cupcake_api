"""Flask app for Cupcakes"""
from flask import Flask, request, jsonify
from models import db, connect_db, Cupcake

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcake_db'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

app.config['SECRET_KEY'] = 'HelloWorld'

connect_db(app)

def serialize_cupcake(cupcake):
    """turns a sqlalchemy obj to dictionary"""
    return {
        "id" : cupcake.id,
        "flavor" : cupcake.flavor,
        "size" : cupcake.size,
        "rating" : cupcake.rating,
        "image" : cupcake.image
    }

@app.route('/api/cupcakes')
def all_cupcakes():
    """Get data about all cupcakes"""
    cupcakes = Cupcake.query.all()
    serialized = [serialize_cupcake(c) for c in cupcakes]

    return jsonify(cupcakes={"cupcakes" : serialized})

@app.route('/api/cupcakes/<int:cupcake_id>')
def single_cupcake(cupcake_id):
    """searches and pulls up info on one cupcake"""
    cupcake = Cupcake.query.get_or_404(cupcake_id)
    serialized = serialize_cupcake(cupcake)

    return jsonify(cupcake = {"cupcake": serialized})

@app.route('/api/cupcakes', methods=["POST"])
def create_cupcake():
    """Adds a cupcake to the database"""
    flavor = request.json["flavor"]
    size = request.json["size"]
    rating = request.json["rating"]
    image = request.json["image"]

    new_cupcake = Cupcake(flavor=flavor,size=size,rating=rating,image=image)

    db.session.add(new_cupcake)
    db.session.commit()

    serialized = serialize_cupcake(new_cupcake)

    return (jsonify(cupcake={"cupcake":serialized}), 201)