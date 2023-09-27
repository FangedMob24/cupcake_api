"""Flask app for Cupcakes"""
from flask import Flask, request, jsonify, render_template
from models import db, Cupcake

def create_app(test_config=None):
    app = Flask(__name__)

    app.config['SECRET_KEY'] = "secret"

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes'
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    else:
        # load the test config if passed in
        app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes_test'
        app.config['SQLALCHEMY_ECHO'] = False
        app.config['TESTING'] = True

    db.init_app(app)

    return app



app = create_app()

@app.route('/')
def home_page():
    return render_template('home.html')

@app.route("/api/cupcakes")
def all_cupcakes():
    """Get data about all cupcakes"""
    cupcakes_list = Cupcake.query.all()
    cupcakes = [c.serialize_cupcake() for c in cupcakes_list]

    return jsonify(cupcakes = cupcakes)

@app.route('/api/cupcakes/<int:cupcake_id>')
def single_cupcake(cupcake_id):
    """searches and pulls up info on one cupcake"""
    cupcake = Cupcake.query.get_or_404(cupcake_id)

    return jsonify(cupcake = cupcake.serialize_cupcake())

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

    serialized = new_cupcake.serialize_cupcake()

    return (jsonify(cupcake=serialized), 201)


@app.route('/api/cupcakes/<int:cupcake_id>', methods=["PATCH"])
def update_cupcake(cupcake_id):
    cupcake = Cupcake.query.get_or_404(cupcake_id)

    cupcake.flavor = request.json.get('flavor', cupcake.flavor)
    cupcake.size = request.json.get('size', cupcake.size)
    cupcake.rating = request.json.get('rating', cupcake.rating)
    cupcake.image = request.json.get('image', cupcake.image)
    db.session.commit()
    
    
    return (jsonify(cupcake=cupcake.serialize_cupcake()), 200)

@app.route('/api/cupcakes/<int:cupcake_id>', methods=["DELETE"])
def delete_cupcake(cupcake_id):
    cupcake = Cupcake.query.get_or_404(cupcake_id)
    db.session.delete(cupcake)
    db.session.commit()
    return (jsonify(message="Deleted"), 200)