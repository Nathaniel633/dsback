from sklearn.tree import DecisionTreeRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split
import pandas as pd
import numpy as np

class FitnessModel:
    """A class used to represent the Fitness Model based on features like Duration, BPM, and Intensity."""
    _instance = None
    
    def __init__(self):
        # Initialize model and data attributes
        self.model = None  # Linear regression model
        self.dt = None  # Decision tree model
        self.features = ['Duration', 'BPM', 'Intensity']  # Features used for prediction
        self.target = 'Calories'  # Target variable
        self.fitness_data = pd.read_csv('fitness.csv')  # Load fitness data from CSV file
    
    def _train(self):
        # Split data into features and target
        X = self.fitness_data[self.features]
        y = self.fitness_data[self.target]
        # Split data into training and testing sets
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        # Train linear regression model
        self.model = LinearRegression()
        self.model.fit(X_train, y_train)
        # Train decision tree model
        self.dt = DecisionTreeRegressor()
        self.dt.fit(X_train, y_train)
    
    @classmethod
    def get_instance(cls):
        """Get a singleton instance of the FitnessModel class."""
        if cls._instance is None:
            cls._instance = cls()
            cls._instance._train()
        return cls._instance
    
    def predict(self, data_point):
        """Predict calorie burn based on given data point."""
        # Create DataFrame from data point
        data_point_df = pd.DataFrame(data_point, index=[0])
        # Predict calorie burn using linear regression model
        calorie_burn = self.model.predict(data_point_df[self.features])[0]
        return calorie_burn
    
    def feature_weights(self):
        """Get feature importance weights from decision tree model."""
        importances = self.dt.feature_importances_
        return {feature: importance for feature, importance in zip(self.features, importances)}

def initFitnessModel():
    """Initialize the FitnessModel singleton instance."""
    FitnessModel.get_instance()

def testFitnessModel():
    """Test the FitnessModel by predicting calorie burn and printing feature weights."""
    print("Step 1: Define data point for prediction:")
    # Define a data point for prediction
    data_point = {
        'Duration': 37,
        'BPM': 170,
        'Intensity': 5
    }
    print("\t", data_point)
    print()
    # Get instance of FitnessModel
    fitnessModel = FitnessModel.get_instance()
    print("Step 2:", fitnessModel.get_instance.__doc__)
    print("Step 3:", fitnessModel.predict.__doc__)
    # Predict calorie burn for the data point
    predicted_calories = fitnessModel.predict(data_point)
    print('\tPredicted Calorie Burn:', predicted_calories)
    print()
    print("Step 4:", fitnessModel.feature_weights.__doc__)
    # Get feature weights (importance) from the model
    importances = fitnessModel.feature_weights()
    for feature, importance in importances.items():
        print("\t", feature, f"{importance:.2%}")

if __name__ == "__main__":
    testFitnessModel()
