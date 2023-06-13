from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy 
from datetime import date
from flask_marshmallow import Marshmallow

app = Flask(__name__)

# set the database URI via SQLAlchemy, 
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://trello_dev:spameggs123@localhost:5432/trello'

#create the database object
db = SQLAlchemy(app)

ma = Marshmallow(app)

class Card(db.Model):
    # define the table name for the db
    __tablename__= "cards"
    # Set the primary key, we need to define that each attribute is also a column in the db table, remember "db" is the object we created in the previous step.
    id = db.Column(db.Integer,primary_key=True)
    # Add the rest of the attributes. 
    title = db.Column(db.String())
    description = db.Column(db.String())
    date = db.Column(db.Date())
    status = db.Column(db.String())
    priority = db.Column(db.String())

#create the Card Schema with Marshmallow, it will provide the serialization needed for converting the data into JSON
class CardSchema(ma.Schema):
    class Meta:
        # Fields to expose
        fields = ("id", "title", "description", "date", "status", "priority")

#single card schema, when one card needs to be retrieved
card_schema = CardSchema()
#multiple card schema, when many cards need to be retrieved
cards_schema = CardSchema(many=True)
# create app's cli command named create, then run it in the terminal as "flask create", 
# it will invoke create_db function
@app.cli.command("create")
def create_db():
    db.drop_all()
    db.create_all()
    print("Tables created for Phillip")

# @app.cli.command("seed")
# def seed_db():
#     from datetime import date
#     # create the card object
#     card1 = Card(
#         # set the attributes, not the id, SQLAlchemy will manage that for us
#         title = "Start the project",
#         description = "Stage 1, creating the database",
#         status = "To Do",
#         priority = "High",
#         date = date.today()
#     )
#     # Add the object as a new row to the table
#     db.session.add(card1)
#     # commit the changes
#     db.session.commit()
#     print("Table seeded for Phillip")  

@app.cli.command('seed')
def seed_db():
    # Create an instance of the card model in memory
    cards = [
        Card(
            title = 'Start the project',
            description = 'Stage 1 - Create an ERD', 
            status = "Done",
            priority = "High",
            date = date.today()
        ),
        Card(
            title = 'PRM Queries',
            description = 'Stage 2 - Implement several queries', 
            status = "In Progress",
            priority = "High",
            date = date.today()
        ),
        Card(
            title = 'Marshmellow',
            description = 'Stage 3 - Implement jsonify of models', 
            status = "In Progress",
            priority = "High",
            date = date.today()
        )
    ]

    # Truncate the Card table
    db.session.query(Card).delete()
    # Add the card to the session (transaction)
    # db.session.add(card)
    db.session.add_all(cards)

    # Commit the tranaction to the database
    db.session.commit()
    print('Models seeded for Phillip')

@app.cli.command("drop")
def drop_db():
    db.drop_all()
    print("Tables dropped for Phillip") 

@app.route("/")
def hello():
    return "Hello Phillip Miguel Markovic!"

@app.route("/cards", methods=["GET"])
def get_cards():
    # get all the cards from the database table
    cards_list = Card.query.all()
    # Convert the cards from the database into a JSON format and store them in result
    result = cards_schema.dump(cards_list)
    # return the data in JSON format
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
