from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import date
from flask_marshmallow import Marshmallow

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://trello_dev:spameggs123@localhost:5432/trello'

db = SQLAlchemy(app)
ma = Marshmallow(app)

# print(db.__dict__)
# print(app.config)


class Card(db.Model):
    __tablename__ = 'cards'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    description = db.Column(db.Text())
    status = db.Column(db.String(30))
    date_created = db.Column(db.Date())

class CardSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'description', 'status')

@app.cli.command('create')
def create_db():
    db.drop_all()
    db.create_all()
    print('Tables created successfully')

@app.cli.command('seed')
def seed_db():
    # Create an instance of the card model in memory
    cards = [
        Card(
            title = 'Start the project',
            description = 'Stage 1 - Create an ERD', 
            status = "Done",
            date_created = date.today()
        ),
        Card(
            title = 'PRM Queries',
            description = 'Stage 2 - Implement several queries', 
            status = "In Progress",
            date_created = date.today()
        ),
        Card(
            title = 'Marshmellow',
            description = 'Stage 3 - Implement jsonify of models', 
            status = "In Progress",
            date_created = date.today()
        )
    ]

    # Truncate the Card table
    db.session.query(Card).delete()
    # Add the card to the session (transaction)
    # db.session.add(card)
    db.session.add_all(cards)

    # Commit the tranaction to the database
    db.session.commit()
    print('Models seeded')

@app.route('/cards')
def all_cards():
    # stmt = db.select(Card).limit(1)
    # stmt = db.select(Card).where(db.or_(Card.status != "Done", Card.id  > 2)).order_by(Card.title.desc())
    # print(stmt)
    # cards = db.session.execute(stmt)
    # print(cards)

    # card = db.session.scalars(stmt).first()
    # print(card)

    stmt = db.select(Card).order_by(Card.status.desc())
    cards = db.session.scalars(stmt).all()
    return CardSchema(many=True).dump(cards)

    # for card in cards:
    #     print(card.__dict__)


@app.route('/')
def index():
    return 'Hello World!'

if __name__ == '__main__':
    app.run(debug=True)

