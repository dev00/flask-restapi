from app import app, db
from flask import Flask, jsonify, request
from sqlalchemy import asc, desc, or_
import requests
from .models import Product

@app.route('/collect')
def collect():
  url = "https://api.zalando.com/articles/"

  # Temp solution to ensure DB gets filled with 600 entries
  parameters = {'pageSize': '200'}
  for i in range(1,4):
    try:
      parameters['page'] = i
      r = requests.get(url, params=parameters)
      items = r.json()
      for item in items['content']:
        product = Product(
                  name = item['name'],
                  price = item['units'][0]['price']['value'],
                  brand = item['brand']['key'],
                  image = item['media']['images'][0]['smallUrl']
                  )
        db.session.add(product)
      app.logger.debug("Added %s products to DB Session" % len(items['content']))
      db.session.commit()

    # Maybe the API will timeout, better catch it 
    except requests.exceptions.Timeout:
      app.logger.error("Connection to the Zalando API timed out, could not fill db")
    except requests.exceptions.HTTPError as e:
      app.logger.error(e)
   
  return jsonify({'msg': 'import successfull'})

@app.route('/')
def index():
 return jsonify({'msg': 'What a wonderfull world'})

@app.route('/all')
def all():
  response = [{
    'name' : i.product_name,
    'price': i.price,
    'brand': i.brand,
    'image': i.image,
    } for i in Product.query.all()]

  # PEP 8 states that empy lists are false
  if not response:
    return jsonify({'msg': 'No data was found. Please populate first'}), 404

  return jsonify(response)

@app.route('/search')
def search():
  # unescaped since SQLAlchemy will escape it for us
  per_page       = request.args.get('per_page', '10')
  q              = '%{q}%'.format(q = request.args.get('q', ''))
  column         = request.args.get('c')
  page           = request.args.get('page', '1')
  sort           = request.args.get('sort', 'price')
  direction      = request.args.get('direction', 'asc')

  sort_allowed      = ['product_name', 'brand', 'price']

  try:
    int(page)
  except ValueError:
    return jsonify({'msg': 'page has to be int'}), 500

  try:
    int(per_page)
  except ValueError:
    return jsonify({'msg': 'per_page has to be int'}), 500

  if sort not in sort_allowed:
    return jsonify({'msg': 'The sort criteria was not allowed.'}), 400

  if direction not in ['asc', 'desc']:
    return jsonify({'msg': 'The sort direction was not allowed.'}), 400

  # get the correct column to sort by and the sort direction
  sorted_column = getattr(getattr(Product, sort), direction)()

  # limit searching to a specific column when correctly defined
  if column in ['product_name', 'brand']:
    criteria = getattr(Product, column).like(q)
  
  # if no column was defined, do full text
  # since fts is not implemented yet, manually select all columns by using or_
  else:
    criteria = or_(Product.brand.like(q), Product.product_name.like(q))
  
  app.logger.debug("Ordering by %s %s" % (sort, direction))

  response = [{
    'name' : i.product_name,
    'price': i.price,
    'brand': i.brand,
    'image': i.image,
  } for i in Product.query.filter(criteria) \
    .order_by(sorted_column).paginate(int(page), int(per_page), False).items
  ]

  if not response:
    return jsonify({'msg': 'No articles were found'}), 404

  return jsonify(response)
