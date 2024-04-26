from sklearn.tree import DecisionTreeRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split
import pandas as pd

class FitnessModel:
    _instance = None
    
    def __init__(self):
        self.model = None
        self.dt = None
        self.features = ['Duration', 'BPM', 'Intensity']
        self.target = 'Calories'
        self.fitness_data = pd.read_csv('fitness.csv')
    
    def _train(self):
        X = self.fitness_data[self.features]
        y = self.fitness_data[self.target]
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        self.model = LinearRegression()
        self.model.fit(X_train, y_train)
        self.dt = DecisionTreeRegressor()
        self.dt.fit(X_train, y_train)
    
    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
            cls._instance._train()
        return cls._instance
    
    def predict(self, data_point):
        data_point_df = pd.DataFrame(data_point, index=[0])
        calorie_burn = self.model.predict(data_point_df[self.features])[0]
        return calorie_burn
    
    def feature_weights(self):
        importances = self.dt.feature_importances_
        return {feature: importance for feature, importance in zip(self.features, importances)}

def initFitnessModel():
    FitnessModel.get_instance()

def testFitnessModel():
    data_point = {
        'Duration': 37,
        'BPM': 170,
        'Intensity': 5
    }
    print("\t", data_point)
    print()
    fitnessModel = FitnessModel.get_instance()
    print("Step 2:", fitnessModel.get_instance.__doc__)
    print("Step 3:", fitnessModel.predict.__doc__)
    predicted_calories = fitnessModel.predict(data_point)
    print('\tPredicted Calorie Burn:', predicted_calories)
    print()
    print("Step 4:", fitnessModel.feature_weights.__doc__)
    importances = fitnessModel.feature_weights()
    for feature, importance in importances.items():
        print("\t", feature, f"{importance:.2%}")

if __name__ == "__main__":
    testFitnessModel()
