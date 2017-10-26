import os
import requests
import unittest

from config import basedir
from app import app, db
from sqlalchemy import asc, desc
from app.models import Product


class TestCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'test.db')
        url = 'https://api.zalando.com/articles/'
        self.app = app.test_client()
        db.create_all()

        r = requests.get(url, params={'pageSize': '200'})
        items = r.json()
        for item in items['content']:
          product = Product(
                    name = item['name'],
                    price = item['units'][0]['price']['value'],
                    brand = item['brand']['key'],
                    image = item['media']['images'][0]['smallUrl']
                    )
          db.session.add(product)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()


    # ensure data import works
    def test_data_collect(self):
        with app.test_client() as c:
            response = c.get('/collect')
            self.assertEqual(response.status_code, 200)
        assert Product.query.first() is not None

    def test_incorrect_sort_colum(self):
        with app.test_client() as c:
            response = c.get('/search?sort=image')
            self.assertEqual(response.status_code, 400)

    def test_plain_sort(self):
        with app.test_client() as c:
            response = c.get('/search')
            self.assertEqual(response.status_code, 200)
            first_product = Product.query.order_by(Product.price.asc()).first()
            last_product = Product.query.order_by(Product.price.desc()).first()
         assert first_product.price < last_product.price

    def test_parametrized_sort(self):
        with app.test_client() as c:
            response = c.get('/search?sort=product_name')
            self.assertEqual(response.status_code, 200)
            first_product = Product.query.order_by(Product.product_name.asc()).first()
            last_product = Product.query.order_by(Product.product_name.desc()).first()
        assert first_product.product_name < last_product.product_name
if __name__ == '__main__':
    unittest.main()
