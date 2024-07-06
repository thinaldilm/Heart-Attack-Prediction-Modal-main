from flask import Flask, render_template, request
import joblib
import pandas as pd

app = Flask(__name__)

# Load your model and columns used for prediction
model = joblib.load('random_forest_model.pkl')
model_columns = joblib.load('model_columns.pkl')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    if request.method == 'POST':
        # Collect input data from the form
        input_data = {
            'Age': int(request.form['age']),
            'Sex': request.form['sex'],
            'Cholesterol': int(request.form['cholesterol']),
            'Blood Pressure': float(request.form['blood_pressure']),
            'Max Heart Rate': int(request.form['max_heart_rate']),
            'Exercise Induced Angina': int(request.form['exercise_induced_angina']),
            'Family History': int(request.form['family_history']),
            'Smoking': int(request.form['smoking']),
            'Obesity': int(request.form['obesity']),
            'Alcohol Consumption': int(request.form['alcohol_consumption']),
            'Exercise Hours Per Week': float(request.form['exercise_hours_per_week']),
            'Diet_Healthy': int(request.form['diet_healthy']),
            'Diet_Unhealthy': int(request.form['diet_unhealthy']),
            'Previous Heart Problems': int(request.form['previous_heart_problems']),
            'Medication Use': int(request.form['medication_use']),
            'Stress Level': int(request.form['stress_level']),
            'Sedentary Hours Per Day': float(request.form['sedentary_hours_per_day']),
            'Income': int(request.form['income']),
            'BMI': float(request.form['bmi']),
            'Triglycerides': int(request.form['triglycerides']),
            'Physical Activity Days Per Week': int(request.form['physical_activity_days_per_week']),
            'Sleep Hours Per Day': int(request.form['sleep_hours_per_day']),
        }

        # Create a DataFrame from the input data
        input_df = pd.DataFrame([input_data])

        # Ensure all required columns are present and in correct order
        for column in model_columns:
            if column not in input_df.columns:
                input_df[column] = 0

        input_df = input_df[model_columns]  # Reorder columns as needed

        # Make prediction using the model
        prediction = model.predict(input_df)
        prediction_text = 'high risk' if prediction[0] == 1 else 'low risk'

        # Render the template with the prediction result
        return render_template('index.html', prediction_text=f'The model predicts a {prediction_text} of heart attack.', **input_data)

if __name__ == '__main__':
    app.run(debug=True)
