from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource, reqparse, Api, fields, marshal_with, abort

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"

api = Api(app)
db = SQLAlchemy(app)

class ItemModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String, nullable=False)
    title = db.Column(db.String, nullable=False)
    cost = db.Column(db.Integer)
    description = db.Column(db.String, nullable=False)

    def __repr__(self):
        return f"Type: {self.type} | Title: {self.title} | Cost: {self.cost} | Description: {self.description}"

item_args = reqparse.RequestParser()
item_args.add_argument("type", type=str, required=True, help="Type cannot be blank.")
item_args.add_argument("title", type=str, required=True, help="Title cannot be blank.")
item_args.add_argument("cost", type=int, required=True, help="Cost cannot be blank.")
item_args.add_argument("description", type=str, required=True, help="Description cannot be blank.")

itemFields = {
    "id": fields.Integer,
    "type": fields.String,
    "title": fields.String,
    "cost": fields.Integer,
    "description": fields.String
}

class Items(Resource):
    @marshal_with(itemFields)
    def get(self):
        items = ItemModel.query.all()
        if not items:
            return [], 200

        return items

    @marshal_with(itemFields)
    def post(self):
        args = item_args.parse_args()
        item = ItemModel(type=args["type"], title=args["title"], cost=args["cost"], description=args["description"])
        db.session.add(item)
        db.session.commit()
        items = ItemModel.query.all()

        return items, 201

class Item(Resource):
    @marshal_with(itemFields)
    def get(self, id):
        item = ItemModel.query.filter_by(id=id).first()
        if not item:
            abort(404, message=f"Item with id {id} not found.")

        return item

    @marshal_with(itemFields)
    def put(self, id):
        item = ItemModel.query.filter_by(id=id).first()
        if not item:
            abort(404, message=f"Item with id {id} not found.")
        args = item_args.parse_args()
        item.type = args["type"]
        item.title = args["title"]
        item.cost = args["cost"]
        item.description = args["description"]
        db.session.commit()

        return item

    @marshal_with(itemFields)
    def delete(self, id):
        item = ItemModel.query.filter_by(id=id).first()
        if not item:
            abort(404, message=f"Item with id {id} not found.")
        db.session.delete(item)
        db.session.commit()
        items = ItemModel.query.all()

        return items

api.add_resource(Items, "/api/items")
api.add_resource(Item, "/api/items/<int:id>")



# @app.route("/")
# def home():
    # return "TEST"