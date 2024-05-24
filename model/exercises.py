from __init__ import db
import pandas as pd

class ExerciseModel(db.Model):
    __tablename__ = 'exercises'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    intensity = db.Column(db.String(20), nullable=False)
    type = db.Column(db.String(50), nullable=False)
    calories_burned = db.Column(db.Integer, nullable=False)
    likes = db.Column(db.Integer, default=0)

    def __init__(self, name, intensity, type, calories_burned, likes=0):
        self.name = name
        self.intensity = intensity
        self.type = type
        self.calories_burned = calories_burned
        self.likes = likes

    @classmethod
    def load_data_from_csv(cls, csv_file):
        exercises_data = pd.read_csv(csv_file)
        for _, row in exercises_data.iterrows():
            new_entry = cls(
                name=row['Exercise'],
                intensity=row['Intensity Level'],
                type=row['Type'],
                calories_burned=row['Calories Burned per Hour'],
                likes=0
            )
            db.session.add(new_entry)
        db.session.commit()

    def increase_likes(self):
        self.likes += 1
        db.session.commit()

def initExerciseModel():
    with db.engine.connect() as connection:
        ExerciseModel.__table__.create(bind=connection, checkfirst=True)
        ExerciseModel.load_data_from_csv('exercise_dataset.csv')
