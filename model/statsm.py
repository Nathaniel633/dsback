from __init__ import app, db
from sqlalchemy.exc import IntegrityError
from datetime import date
from random import randrange
class Stats(db.Model):
    __tablename__ = 'stats'
    id = db.Column(db.Integer, primary_key=True)
    playerName = db.Column(db.String, nullable=False)
    goals = db.Column(db.Integer, nullable=False)
    number = db.Column(db.Integer, nullable=False)
    uid = db.Column(db.Integer, db.ForeignKey('users.id'))
    def __init__(self, uid, playerName, goals, number):
        self.uid = uid
        self.playerName = playerName
        self.goals = goals
        self.number = number
    def __repr__(self):
        return f"Stats(id={self.number}, uid={self.uid})"
    def create(self):
        try:
            db.session.add(self)
            db.session.commit()
            return self
        except IntegrityError:
            db.session.rollback()
            return None
    def read(self):
        return {
            # "id": self.id,
            "uid": self.uid,
            "playerName": self.playerName,
            "goals": self.goals,
            "number": self.number
        }
def initStats():
    with app.app_context():
        db.create_all()
        u1 = Stats(uid=1, playerName='demi l', goals=13, number=11)
        u2 = Stats(uid=2, playerName='moer j', goals=23, number=20)
        stats = [u1, u2]
        for stat in stats:
            try:
                stat.create()
            except IntegrityError:
                db.session.rollback()
                print(f"Error creating stat: {stat}")