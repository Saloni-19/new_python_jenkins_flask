# -*- coding: utf-8 -*-
"""
Created on Wed Jan 27 10:51:43 2021

@author: SaloniKhandelwal

#In node js Rest API
app = express()
app.get('',())
app.post('',())
"""

import json
from flask import Flask,jsonify,request,Response,make_response
from flask_sqlalchemy import SQLAlchemy
from marshmallow_sqlalchemy import ModelSchema
from marshmallow import fields

app = Flask(__name__)     #implicit reference to the current module name...Using single module __name__ (exposing __name__ as module---> read current file)

app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://admin:admin@localhost:3306/devops'

db = SQLAlchemy(app)


class Product(db.Model):
    __tablename__="pyproducts"
    productId = db.Column(db.Integer,primary_key=True)
    productName = db.Column(db.String(40))
    description = db.Column(db.String(40))
    productCode = db.Column(db.String(40))
    price = db.Column(db.Float)
    starRating = db.Column(db.Float)
    imageUrl = db.Column(db.String(40))
    
    def create(self):
        db.session.add(self)
        db.session.commit()
        return self
    def __init__(self,productName,description,productCode,price,starRating,imageUrl):
        self.productName = productName
        self.description = description
        self.productCode = productCode
        self.price = price
        self.starRating = starRating
        self.imageUrl = imageUrl
    def __repr__(self):                 #String representation of an object-->__str__ does the same-->>Difference---> in official string representation we use __repr__---->>> if we call print then __str__ is used
        return "% self.productId"
        
db.create_all()                         #this function will create the table


#Flask will take care of mapping of objects to table, also take care of low level sql queries and operations
 
#map object to table 
#get object representation of object      
class ProductSchema(ModelSchema):
    class Meta(ModelSchema.Meta):
        model = Product
        sqla_session = db.session
    productId = fields.Number(dump_only=True)                       #Auto Generated
    productName = fields.String(required=True)
    description = fields.String(required=True)
    productCode = fields.String(required=True)
    price = fields.Number(required=True)
    starRating = fields.Number(required=True)
    imageUrl = fields.String(required=True)

#http://localhost:4002/products
@app.route('/products',methods=['POST'])
def createProduct():
    data = request.get_json()
    product_schema = ProductSchema()
    product = product_schema.load(data)                             #Unmarshing (mapping json data to object)---> get product object
    result = product_schema.dump(product.create())                  #Flask will create insert query by create() method
    return make_response(jsonify({"product":result}),201)           #201-successfully executed and new object is created

@app.route('/products',methods=['GET'])
def getAllProducts():
    get_products = Product.query.all()
    productSchema = ProductSchema(many=True)
    products = productSchema.dump(get_products)
    return make_response(jsonify({"products":products}),200)

@app.route('/products/<int:productId>',methods=['GET'])
def getProductById(productId):                                       #dependency Injection <int:productId>
    get_product = Product.query.get(productId)
    productSchema = ProductSchema()
    product = productSchema.dump(get_product)
    return make_response(jsonify({"product":product}),200)           #default state code is 200

@app.route('/products/<int:productId>',methods=['DELETE'])
def deleteProductById(productId):                                       #dependency Injection <int:productId>
    get_product = Product.query.get(productId)
    db.session.delete(get_product)
    db.session.commit()
    return make_response(jsonify({"result":"product deleted"}),204)           #204-->no content

@app.route('/products/<int:productId>',methods=['PUT'])
def updateProduct(productId):
    data = request.get_json()
    get_product = Product.query.get(productId)
    if data.get('price'):
        get_product.price = data['price']
    db.session.add(get_product)
    db.session.commit()
    product_schema = ProductSchema(only=['productId','price'])
    result = product_schema.dump(get_product)                  
    return make_response(jsonify({"product":result}),200)           

@app.route('/products/find/<productName>',methods=['GET'])
def getProductByName(productName):                                       #dependency Injection <int:productId>
    get_products = Product.query.filter_by(productName=productName)
    productSchema = ProductSchema(many=True)
    products = productSchema.dump(get_products)
    return make_response(jsonify({"product":products}),200)           #default state code is 200

app.run(port=4002)                      

    
    
    