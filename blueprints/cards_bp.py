from flask import Blueprint, request
from datetime import timedelta
from models.user import User, UserSchema
from models.card import Card, CardSchema
from init import db, bcrypt
from sqlalchemy.exc import IntegrityError
from flask_jwt_extended import create_access_token
from datetime import timedelta

@app.route('/cards')
@jwt_required()
def all_cards():
    admin_required()

    # Select * from cards;
    stmt = db.select(Card).order_by(Card.status.desc())
    cards = db.session.scalars(stmt).all()
    # passing many=True so it returns more than one card
    return CardSchema(many=True).dump(cards)

    # for card in cards:
    #     print(card.__dict__)
