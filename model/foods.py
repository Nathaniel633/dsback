from sklearn.tree import DecisionTreeRegressor
from sklearn.model_selection import train_test_split
import pandas as pd
from __init__ import app, db

class FoodModel(db.Model):
    # establish schema in SQlite database
    __tablename__ = 'food_data'
    id = db.Column(db.Integer, primary_key=True)
    steps = db.Column(db.Integer, nullable=False)  
    stress = db.Column(db.Integer, nullable=False)  
    meditation = db.Column(db.Integer, nullable=False)  
    produce = db.Column(db.Float, nullable=False)  

    def __init__(self, steps, stress, meditation, produce): 
        self.steps = steps  
        self.stress = stress 
        self.meditation = meditation  
        self.produce = produce 

    @classmethod
    # Iterate through the .csv and append to the database
    def load_data_from_csv(cls, csv_file):
        food_data = pd.read_csv(csv_file)
        for _, row in food_data.iterrows():
            new_entry = cls(
                steps=row['Steps'],  
                stress=row['Stress'],  
                meditation=row['Meditation'], 
                produce=row['Produce']  
            )
            db.session.add(new_entry)
        db.session.commit()

    @classmethod
    def train_model(cls):
        # Set Steps, stress, and meditation as independent variables
        X = pd.DataFrame([(entry.steps, entry.stress, entry.meditation) for entry in cls.query.all()],
                         columns=['Steps', 'Stress', 'Meditation'])
        # Set Produce as dependent variable
        y = pd.DataFrame([entry.produce for entry in cls.query.all()], columns=['Produce'])

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # Train decision tree model
        cls.dt_model = DecisionTreeRegressor()
        cls.dt_model.fit(X_train, y_train)

    @classmethod
    def predict_produce(cls, steps, stress, meditation):
        data_point = pd.DataFrame({'Steps': [steps], 'Stress': [stress], 'Meditation': [meditation]})
        
        # Predict using the decision tree model
        produce_pred_dt = cls.dt_model.predict(data_point)[0]

        return int(produce_pred_dt)
    def serialize(self):
        return {
            'id': self.id,
            'steps': self.steps,
            'stress': self.stress,
            'meditation': self.meditation,
            'produce': self.produce
        }
    def delete(self):
        db.session.delete(self)
        db.session.commit()
        return None

def initFoodModel():
    with db.engine.connect() as connection:
        FoodModel.__table__.create(bind=connection, checkfirst=True)  # Create table if not exists
        FoodModel.load_data_from_csv('food.csv')
        FoodModel.train_model()