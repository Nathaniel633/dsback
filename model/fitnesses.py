from sklearn.tree import DecisionTreeRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split
import pandas as pd
import numpy as np
from random import randrange
from datetime import date
import os, base64
import json
import sqlite3

from __init__ import app, db
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash, check_password_hash

class FitnessModel(db.Model):
    __tablename__ = 'fitness_data'

    id = db.Column(db.Integer, primary_key=True)
    duration = db.Column(db.Integer, nullable=False)
    bpm = db.Column(db.Integer, nullable=False)
    intensity = db.Column(db.Integer, nullable=False)
    calories = db.Column(db.Float, nullable=False)

    def __init__(self, duration, bpm, intensity, calories):
        self.duration = duration
        self.bpm = bpm
        self.intensity = intensity
        self.calories = calories

    @classmethod
    def load_data_from_csv(cls, csv_file):
        fitness_data = pd.read_csv(csv_file)
        for _, row in fitness_data.iterrows():
            new_entry = cls(
                duration=row['Duration'],
                bpm=row['BPM'],
                intensity=row['Intensity'],
                calories=row['Calories']
            )
            db.session.add(new_entry)
        db.session.commit()

    @classmethod
    def train_model(cls):
        X = pd.DataFrame([(entry.duration, entry.bpm, entry.intensity) for entry in cls.query.all()],
                         columns=['Duration', 'BPM', 'Intensity'])
        y = pd.DataFrame([entry.calories for entry in cls.query.all()], columns=['Calories'])

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # Train decision tree model
        cls.dt_model = DecisionTreeRegressor()
        cls.dt_model.fit(X_train, y_train)

    @classmethod
    def predict_calories(cls, duration, bpm, intensity):
        data_point = pd.DataFrame({'Duration': [duration], 'BPM': [bpm], 'Intensity': [intensity]})
        
        # Predict using the decision tree model
        calorie_pred_dt = cls.dt_model.predict(data_point)[0]
        print(calorie_pred_dt)

        return int(calorie_pred_dt)

    @classmethod
    def testFitnessModel(cls):
        # Load data and train model
        cls.load_data_from_csv('fitness.csv')
        cls.train_model()

        # Test example data points
        test_data_points = [
            {'duration': 37, 'bpm': 170, 'intensity': 5},
            {'duration': 45, 'bpm': 160, 'intensity': 4},
            {'duration': 30, 'bpm': 180, 'intensity': 6}
        ]

        print("Testing Fitness Model Predictions:")
        for data_point in test_data_points:
            duration = data_point['duration']
            bpm = data_point['bpm']
            intensity = data_point['intensity']
            
            predicted_calories = cls.predict_calories(duration, bpm, intensity)
            print(f"For Duration={duration}, BPM={bpm}, Intensity={intensity}: Predicted Calories={predicted_calories}")

def initFitnessModel():
    with db.engine.connect() as connection:
        FitnessModel.__table__.create(bind=connection, checkfirst=True)  # Create table if not exists
        FitnessModel.load_data_from_csv('fitness.csv')
        FitnessModel.train_model()


# class FitnessModel(db.model):
#     """A class used to represent the Fitness Model based on features like Duration, BPM, and Intensity."""
#     _instance = None
    
#     def __init__(self):
#         # Initialize model and data attributes
#         self.model = None  # Linear regression model
#         self.dt = None  # Decision tree model
#         self.features = ['Duration', 'BPM', 'Intensity']  # Features used for prediction
#         self.target = 'Calories'  # Target variable
#         self.fitness_data = pd.read_csv('fitness.csv')  # Load fitness data from CSV file
    
#     def _train(self):
#         # Split data into features and target
#         X = self.fitness_data[self.features]
#         y = self.fitness_data[self.target]
#         # Split data into training and testing sets
#         X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
#         # Train linear regression model
#         self.model = LinearRegression()
#         self.model.fit(X_train, y_train)
#         # Train decision tree model
#         self.dt = DecisionTreeRegressor()
#         self.dt.fit(X_train, y_train)
    
#     @classmethod
#     def get_instance(cls):
#         """Get a singleton instance of the FitnessModel class."""
#         if cls._instance is None:
#             cls._instance = cls()
#             cls._instance._train()
#         return cls._instance
    
#     def predict(self, data_point):
#         """Predict calorie burn based on given data point."""
#         # Create DataFrame from data point
#         data_point_df = pd.DataFrame(data_point, index=[0])
#         # Predict calorie burn using linear regression model
#         calorie_burn = self.model.predict(data_point_df[self.features])[0]
#         return calorie_burn
    
#     def feature_weights(self):
#         """Get feature importance weights from decision tree model."""
#         importances = self.dt.feature_importances_
#         return {feature: importance for feature, importance in zip(self.features, importances)}

# def initFitnessModel():
#     """Initialize the FitnessModel singleton instance."""
#     FitnessModel.get_instance()

# def testFitnessModel():
#     """Test the FitnessModel by predicting calorie burn and printing feature weights."""
#     print("Step 1: Define data point for prediction:")
#     # Define a data point for prediction
#     data_point = {
#         'Duration': 37,
#         'BPM': 170,
#         'Intensity': 5
#     }
#     print("\t", data_point)
#     print()
#     # Get instance of FitnessModel
#     fitnessModel = FitnessModel.get_instance()
#     print("Step 2:", fitnessModel.get_instance.__doc__)
#     print("Step 3:", fitnessModel.predict.__doc__)
#     # Predict calorie burn for the data point
#     predicted_calories = fitnessModel.predict(data_point)
#     print('\tPredicted Calorie Burn:', predicted_calories)
#     print()
#     print("Step 4:", fitnessModel.feature_weights.__doc__)
#     # Get feature weights (importance) from the model
#     importances = fitnessModel.feature_weights()
#     for feature, importance in importances.items():
#         print("\t", feature, f"{importance:.2%}")

# if __name__ == "__main__":
#     testFitnessModel()

# import sqlite3
# import pandas as pd
# from sklearn.tree import DecisionTreeRegressor
# from sklearn.linear_model import LinearRegression
# from sklearn.model_selection import train_test_split

# class FitnessModel:
#     """A class used to represent the Fitness Model based on features like Duration, BPM, and Intensity."""
#     _instance = None
    
#     def __init__(self):
#         # Initialize model and data attributes
#         self.model = LinearRegression  # Linear regression model
#         self.dt = None  # Decision tree model
#         self.features = ['Duration', 'BPM', 'Intensity']  # Features used for prediction
#         self.target = 'Calories'  # Target variable
        
#         # Initialize SQLite database and create table from CSV data
#         self._initialize_database_from_csv()
    
#     def _initialize_database_from_csv(self):
#         """Initialize SQLite database and create table from CSV data."""
#         # Connect to SQLite database
#         conn = sqlite3.connect('sqlite.db')
        
#         # Read fitness data from CSV file
#         fitness_data = pd.read_csv('fitness.csv')
        
#         # Store DataFrame in SQLite database as a table named 'fitness_data'
#         fitness_data.to_sql('fitness_data', conn, if_exists='replace', index=False)
        
#         # Commit changes and close connection
#         conn.commit()
#         conn.close()
    
#     def _train(self):
#         # Connect to SQLite database
#         conn = sqlite3.connect('fitness.db')
        
#         # Retrieve data from SQLite database
#         query = "SELECT * FROM fitness_data"
#         fitness_data = pd.read_sql_query(query, conn)
#         conn.close()
        
#         # Split data into features and target
#         X = fitness_data[self.features]
#         y = fitness_data[self.target]
        
#         # Split data into training and testing sets
#         X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
#         # Train linear regression model
#         self.model = LinearRegression()
#         self.model.fit(X_train, y_train)
        
#         # Train decision tree model
#         self.dt = DecisionTreeRegressor()
#         self.dt.fit(X_train, y_train)
    
#     @classmethod
#     def get_instance(cls):
#         """Get a singleton instance of the FitnessModel class."""
#         if cls._instance is None:
#             cls._instance = cls()
#             cls._instance._train()
#         return cls._instance
    
#     def predict(self, data_point):
#         """Predict calorie burn based on given data point."""
#         # Create DataFrame from data point
#         data_point_df = pd.DataFrame(data_point, index=[0])
        
#         # Predict calorie burn using linear regression model
#         calorie_burn = self.model.predict(data_point_df[self.features])[0]
        
#         return calorie_burn
    
#     def feature_weights(self):
#         """Get feature importance weights from decision tree model."""
#         importances = self.dt.feature_importances_
#         return {feature: importance for feature, importance in zip(self.features, importances)}

# def initFitnessModel():
#     """Initialize the FitnessModel singleton instance."""
#     FitnessModel.get_instance()

# def testFitnessModel():
#     """Test the FitnessModel by predicting calorie burn and printing feature weights."""
#     print("Step 1: Define data point for prediction:")
    
#     # Define a data point for prediction
#     data_point = {
#         'Duration': 37,
#         'BPM': 170,
#         'Intensity': 5
#     }
    
#     print("\t", data_point)
#     print()
    
#     # Get instance of FitnessModel
#     fitnessModel = FitnessModel.get_instance()
    
#     print("Step 2:", fitnessModel.get_instance.__doc__)
#     print("Step 3:", fitnessModel.predict.__doc__)
    
#     # Predict calorie burn for the data point
#     predicted_calories = fitnessModel.predict(data_point)
#     print('\tPredicted Calorie Burn:', predicted_calories)
#     print()
    
#     print("Step 4:", fitnessModel.feature_weights.__doc__)
    
#     # Get feature weights (importance) from the model
#     importances = fitnessModel.feature_weights()
    
#     for feature, importance in importances.items():
#         print("\t", feature, f"{importance:.2%}")

# if __name__ == "__main__":
#     # Initialize FitnessModel and perform tests
#     initFitnessModel()
#     testFitnessModel()
