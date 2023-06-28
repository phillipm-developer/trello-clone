from init import db, ma
from marshmallow import fields

class Comment(db.Model):
    __tablename__ = 'comments'

    id = db.Column(db.Integer, primary_key=True)

    message = db.Column(db.Text())
    status = db.Column(db.String(30))
    date_created = db.Column(db.Date())

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user = db.relationship('User', back_populates='comments')

    card_id = db.Column(db.Integer, db.ForeignKey('cards.id'), nullable=False)
    card = db.relationship('Card', back_populates='comments')

class CommentSchema(ma.Schema):
    # Tell marshmallow to use UserSchema to serialize 'user' field
    # user = fields.Nested('UserSchema', exclude=['password', 'cards', 'comments'])
    user = fields.Nested('UserSchema', only=['name', 'email', 'is_admin'])
    card = fields.Nested('CardSchema', only=['title', 'description', 'status'])

    class Meta:
        fields = ('id', 'message', 'date_created', 'status', 'user', 'card')
        ordered=True
