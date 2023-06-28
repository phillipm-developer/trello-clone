from flask import Blueprint, request, abort
from models.card import Card, CardSchema
from init import db
from flask_jwt_extended import jwt_required
from blueprints.auth_bp import admin_required
from datetime import date

cards_bp = Blueprint('cards', __name__, url_prefix='/cards')

# Get all the cards
@cards_bp.route('/')
@jwt_required()
def all_cards():
    # admin_required()

    # Select * from cards;
    stmt = db.select(Card).order_by(Card.status.desc())
    cards = db.session.scalars(stmt).all()
    # passing many=True so it returns more than one card
    return CardSchema(many=True).dump(cards)

    # for card in cards:
    #     print(card.__dict__)

# Get one card
@cards_bp.route('/<int:card_id>')
@jwt_required()
def one_card(card_id):
    # You can call admin_required() here to protect this route and ensure
    # only admins can use this route.

    stmt = db.select(Card).filter_by(id=card_id)
    card = db.session.scalar(stmt)
    if card:
        return CardSchema().dump(card)
    else:
        # 404 can be any resource not just page
        return {'error': 'Card not found'}, 404

# Create a new card
@cards_bp.route('/', methods=['POST'])
@jwt_required()
def create_card():
    # Load the incoming POST data via the Schema
    card_info = CardSchema().load(request.json)

    # Craete a new Card instance from the card_info
    card = Card(
        title = card_info['title'],
        description = card_info['description'],
        status = card_info['status'],
        date_created = date.today(),
        user_id = card_info['user_id']
    )
    # Add and commit the new card to the session
    db.session.add(card)
    db.session.commit()

    # Send the new card back to the client
    return CardSchema().dump(card), 201

# Update a card
@cards_bp.route('/<int:card_id>', methods=['PUT', 'PATCH'])
@jwt_required()
def update_card(card_id):
    admin_required()

    stmt = db.select(Card).filter_by(id=card_id)
    card = db.session.scalar(stmt)
    card_info = CardSchema().load(request.json)

    if card:
        card.title = card_info.get('title', card.title)
        card.description = card_info.get('description', card.description)
        card.status = card_info.get('status', card.description)
        db.session.commit()
        return CardSchema().dump(card)
    else:
        # 404 can be any resource not just page
        return {'error': 'Card not found'}, 404

# Delete a card 
@cards_bp.route('/<int:card_id>', methods=['DELETE'])
@jwt_required()
def delete_card(card_id):
    admin_required()
    stmt = db.select(Card).filter_by(id=card_id)
    card = db.session.scalar(stmt)
    if card:
        db.session.delete(card)
        db.session.commit()
        return {}, 200
    else:
        # 404 can be any resource not just page
        return {'error': 'Card not found'}, 404
