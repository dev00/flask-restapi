from app import db

class Product(db.Model):
    __tablename = "products"
    def __init__(self, name, price, brand, image):
        self.product_name  = name
        self.price = price
        self.brand = brand
        self.image = image

    id = db.Column(db.Integer, primary_key=True)
    product_name =  db.Column(db.String(50), index=True)
    price = db.Column(db.Float())
    brand = db.Column(db.String(20))
    image = db.Column(db.String(200))

    def __repr__(self):
        return "<Product %s>, <Brand> %s, %s" % (self.product_name, self.brand, self.price)
