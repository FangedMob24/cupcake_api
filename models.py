"""Models for Cupcake app."""
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

Default_cupcake = "https://tinyurl.com/demo-cupcake"

class Cupcake(db.Model):
    """Cupcake information"""

    __tablename__ = "cupcakes"

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)

    flavor = db.Column(db.Text,
                       nullable=False)

    size = db.Column(db.Text,
                     nullable=False)

    rating = db.Column(db.Float,
                      nullable=False)

    image = db.Column(db.Text,
                      nullable=False,
                      default=Default_cupcake)
    
    def serialize_cupcake(self):
        """turns a sqlalchemy obj to dictionary"""
        return {
            "id" : self.id,
            "flavor" : self.flavor,
            "size" : self.size,
            "rating" : self.rating,
            "image" : self.image
        }