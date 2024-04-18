from random import randrange
from datetime import date
import os, base64
import json

from __init__ import app, db
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash, check_password_hash

# Define the Sleep class to represent the 'sleep' table in the database
class Sleep(db.Model):
    __tablename__ = 'sleep'

    _id = db.Column(db.Integer, primary_key=True)
    _gender = db.Column(db.String(10), nullable=False)
    _age = db.Column(db.Integer, nullable=False)
    _occupation = db.Column(db.String(100), nullable=False)
    _sleep_duration = db.Column(db.Float, nullable=False)
    _quality_of_sleep = db.Column(db.Integer, nullable=False)
    _physical_activity_level = db.Column(db.Integer, nullable=False)
    _stress_level = db.Column(db.Integer, nullable=False)
    _bmi_category = db.Column(db.String(20), nullable=False)
    _blood_pressure = db.Column(db.String(10), nullable=False)
    _heart_rate = db.Column(db.Integer, nullable=False)
    _daily_steps = db.Column(db.Integer, nullable=False)
    _sleep_disorder = db.Column(db.String(100), nullable=True)  # Assuming it can be NULL



    def __init__(self, id, gender, age, occupation, sleep_duration, quality_of_sleep, physical_activity_level, stress_level, bmi_category, blood_pressure, heart_rate, daily_steps, sleep_disorder):
        self._id = id
        self._gender = gender
        self._age = age
        self._occupation = occupation
        self._sleep_duration = sleep_duration
        self._quality_of_sleep = quality_of_sleep
        self._physical_activity_level = physical_activity_level
        self._stress_level = stress_level
        self._bmi_category = bmi_category
        self._blood_pressure = blood_pressure
        self._heart_rate = heart_rate
        self._daily_steps = daily_steps
        self._sleep_disorder = sleep_disorder

    # Getters and setters for properties
    @property
    def id(self):
        return self._id
    
    @id.setter
    def id(self, value):
        self._id = value
    
    @property
    def gender(self):
        return self._gender
    
    @gender.setter
    def gender(self, value):
        self._gender = value
    
    @property
    def age(self):
        return self._age
    
    @age.setter
    def age(self, value):
        self._age = value
    
    @property
    def occupation(self):
        return self._occupation
    
    @occupation.setter
    def occupation(self, value):
        self._occupation = value
    
    @property
    def sleep_duration(self):
        return self._sleep_duration
    
    @sleep_duration.setter
    def sleep_duration(self, value):
        self._sleep_duration = value
    
    @property
    def quality_of_sleep(self):
        return self._quality_of_sleep
    
    @quality_of_sleep.setter
    def quality_of_sleep(self, value):
        self._quality_of_sleep = value
    
    @property
    def physical_activity_level(self):
        return self._physical_activity_level
    
    @physical_activity_level.setter
    def physical_activity_level(self, value):
        self._physical_activity_level = value
    
    @property
    def stress_level(self):
        return self._stress_level
    
    @stress_level.setter
    def stress_level(self, value):
        self._stress_level = value
    
    @property
    def bmi_category(self):
        return self._bmi_category
    
    @bmi_category.setter
    def bmi_category(self, value):
        self._bmi_category = value
    
    @property
    def blood_pressure(self):
        return self._blood_pressure
    
    @blood_pressure.setter
    def blood_pressure(self, value):
        self._blood_pressure = value
    
    @property
    def heart_rate(self):
        return self._heart_rate
    
    @heart_rate.setter
    def heart_rate(self, value):
        self._heart_rate = value
    
    @property
    def daily_steps(self):
        return self._daily_steps
    
    @daily_steps.setter
    def daily_steps(self, value):
        self._daily_steps = value
    
    @property
    def sleep_disorder(self):
        return self._sleep_disorder
    
    @sleep_disorder.setter
    def sleep_disorder(self, value):
        self._sleep_disorder = value


    def __str__(self):
        return json.dumps(self.read())
    
    def create(self):
        try:
            # creates a drink object from Drink(db.Model) class, passes initializers
            db.session.add(self)  # add prepares to persist drink object to drinks table
            db.session.commit()  # SqlAlchemy "unit of work pattern" requires a manual commit
            return self
        except IntegrityError:
            db.session.remove()
            return None

    def read(self):
        return {
            "id": self.id,
            "gender": self.gender,
            "age": self.age,
            "occupation": self.occupation,
            "sleep_duration": self.sleep_duration,
            "quality_of_sleep": self.quality_of_sleep,
            "physical_activity_level": self.physical_activity_level,
            "stress_level": self.stress_level,
            "bmi_category": self.bmi_category,
            "blood_pressure": self.blood_pressure,
            "heart_rate": self.heart_rate,
            "daily_steps": self.daily_steps,
            "sleep_disorder": self.sleep_disorder
        }


    def update(self, **kwargs):
        for attr, value in kwargs.items():
            if value and hasattr(self, attr):
                setattr(self, attr, value)
        db.session.commit()
        return self

    def delete(self):
        db.session.delete(self)
        db.session.commit()
        return None



# Initialize the sleep table with data from the CSV file
def init_sleep():
    with app.app_context():
        """Create database and tables"""
        db.create_all()
        """Tester data for table"""
        #s1 = Sleep(_id=1, _gender='Male', _age=27, _occupation='Software Engineer', _sleep_duration=6.1, _quality_of_sleep=6, _physical_activity_level=42, _stress_level=6, _bmi_category='Overweight', _blood_pressure='126/83', _heart_rate=77, _daily_steps=4200, _sleep_disorder=None)
        #s2 = Sleep(_id=2, _gender='Male', _age=28, _occupation='Doctor', _sleep_duration=6.2, _quality_of_sleep=6, _physical_activity_level=60, _stress_level=8, _bmi_category='Normal', _blood_pressure='125/80', _heart_rate=75, _daily_steps=10000, _sleep_disorder=None)


    # List to store Sleep objects
    # Initialize an empty list to store Sleep objects
        sleeps_to_add = []

        # Read data from the JSON file
        try:
            with open(r'sleep.json', 'r') as json_file:
                data = json.load(json_file)
        except Exception as error:
            print("Failed to read JSON file:")

        # Loop through each entry in the JSON data and create Sleep objects
        for item in data:
            s_toadd = Sleep(
                id=item['Person ID'],
                gender=item['Gender'],
                age=item['Age'],
                occupation=item['Occupation'],
                sleep_duration=item['Sleep Duration'],
                quality_of_sleep=item['Quality of Sleep'],
                physical_activity_level=item['Physical Activity Level'],
                stress_level=item['Stress Level'],
                bmi_category=item['BMI Category'],
                blood_pressure=item['Blood Pressure'],
                heart_rate=item['Heart Rate'],
                daily_steps=item['Daily Steps'],
                sleep_disorder=item['Sleep Disorder']
            )
            sleeps_to_add.append(s_toadd)

        # Adding the Sleep objects to the database
        for s in sleeps_to_add:
            try:
                s.create()
            except IntegrityError:
                '''fails with bad or duplicate data'''
                db.session.remove()
                print(f"Records exist, duplicate entry, or error: {sleep}")



@app.route('/api/sleeps', methods=['GET'])
def get_sleeps():
    # Extract query parameter for filtering (sleep_duration)
    sleep_duration = request.args.get('sleep_duration')

    # Query the database for sleep records with the specified duration
    if sleep_duration is not None:
        sleeps = Sleep.query.filter_by(_sleep_duration=float(sleep_duration)).all()
    else:
        # If no sleep duration is provided, return all sleep records
        sleeps = Sleep.query.all()
    
    # Convert queried sleep records to JSON format
    sleep_list = [{'id': sleep.id, 'duration': sleep.sleep_duration} for sleep in sleeps]
    
    # Return JSON response
    return jsonify(sleep_list)



# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
            