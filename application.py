from flask import Flask, render_template, request, redirect, jsonify
from flask_cors import CORS, cross_origin
import pickle
import pandas as pd
import numpy as np

app = Flask(__name__)
cors = CORS(app)
model = pickle.load(open('LinearRegressionModel.pkl', 'rb'))
car = pd.read_csv('quikr car dataset.csv')


@app.route('/', methods=['GET', 'POST'])
def index():
    companies = sorted(car['company'].unique())
    car_models = sorted(car['name'].unique())
    year = sorted(car['year'].unique(), reverse=True)
    fuel_type = car['fuel_type'].unique()

    companies.insert(0, 'Select Company')

    return render_template('index.html', companies=companies, car_models=car_models, years=year, fuel_types=fuel_type)


@app.route('/predict', methods=['POST'])
@cross_origin()
def predict():
    try:
        company = request.form.get('company')
        car_model = request.form.get('car_models')
        year = request.form.get('year')
        fuel_type = request.form.get('fuel_type')
        driven = request.form.get('kilo_driven')

        # Input validation - return plain text for errors to match expected response format
        if company == 'Select Company' or not company:
            return "Please select a company", 400
        
        if not car_model:
            return "Please select a car model", 400
            
        if not year:
            return "Please select a year", 400
            
        if not fuel_type:
            return "Please select a fuel type", 400
            
        if not driven:
            return "Please enter kilometers driven", 400

        # Convert inputs to appropriate types
        try:
            year = int(year)
            driven = int(driven)
        except (ValueError, TypeError):
            return "Year and kilometers driven must be valid numbers", 400

        # Create input DataFrame
        input_data = pd.DataFrame({
            'name': [car_model],
            'company': [company],
            'year': [year],
            'kms_driven': [driven],
            'fuel_type': [fuel_type]
        })

        # Make prediction
        prediction = model.predict(input_data)
        result = np.round(prediction[0], 2)
        print(f"Prediction result: {result}")

        # Return just the number as a string to match the original format
        return str(result)

    except Exception as e:
        app.logger.error(f"Error in prediction: {str(e)}")
        return f"Error: {str(e)}", 500


if __name__ == '__main__':
    app.run(debug=True)