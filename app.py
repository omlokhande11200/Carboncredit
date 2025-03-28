import pickle
from flask import Flask, render_template, request, jsonify
import xgboost as xgb
from flask_cors import CORS


prediction_value=0

app = Flask(__name__)
CORS(app, origins=["http://localhost:3000"])
# Load the trained XGBoost model and scaler
with open('model/model_xgb.pkl', 'rb') as f:
    model = pickle.load(f)

with open('model/scaler.pkl', 'rb') as f:
    scaler = pickle.load(f)

# Home route (frontend)
@app.route('/')
def home():
    return render_template('index.html')

# API route to predict carbon credits
@app.route('/predict', methods=['POST'])
def predict():
    global prediction_value
    try:
        # Extract the features from the frontend form
        fuel_type = request.form.get("fuel_type")
        energy_consumption = float(request.form.get("energy_consumption"))
        raw_materials_used = float(request.form.get("raw_materials_used"))
        co2_emissions = float(request.form.get("co2_emissions"))
        ch4_emissions = float(request.form.get("ch4_emissions"))
        n2o_emissions = float(request.form.get("n2o_emissions"))
        particulate_matter = float(request.form.get("particulate_matter"))
        flow_rate = float(request.form.get("flow_rate"))
        temperature = float(request.form.get("temperature"))
        pressure = float(request.form.get("pressure"))
        gas_sensor_readings = float(request.form.get("gas_sensor_readings"))
        emission_factor = float(request.form.get("emission_factor"))
        carbon_intensity = float(request.form.get("carbon_intensity"))
        co2_capture = float(request.form.get("co2_capture"))

        # Create a feature vector from the form data
        features = [
            energy_consumption,
            raw_materials_used,
            co2_emissions,
            ch4_emissions,
            n2o_emissions,
            particulate_matter,
            flow_rate,
            temperature,
            pressure,
            gas_sensor_readings,
            emission_factor,
            carbon_intensity,
            co2_capture
        ]

        print("Features:", features)  # Debug: print the input features

        # Scale the input data
        scaled_features = scaler.transform([features])

        # Make prediction using the XGBoost model
        prediction = model.predict(scaled_features)

        # Convert the prediction to a native Python float to ensure JSON serialization
        prediction_value = int(round(float(prediction[0])))

        # Return the prediction result as a JSON response
        return jsonify({'prediction': prediction_value})

    except Exception as e:
        print("Error:", e)  # Debug: print the error message in the Flask log
        # Return error message as JSON
        return jsonify({'error': 'An error occurred during prediction. Please check the input data and try again.'})
    
# API route to fetch carbon credits
@app.route('/fetch', methods=['POST'])
def fetch():
    return jsonify({'prediction': prediction_value})

if __name__ == '__main__':
    app.run(debug=True)
