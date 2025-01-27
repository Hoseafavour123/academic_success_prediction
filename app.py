from flask import Flask, render_template, request
import pickle

app = Flask(__name__)

# Load your trained model
with open("academic_success_model.pkl", "rb") as file:
    model = pickle.load(file)


def generate_message(prediction):
    """Generate a personalized message based on the prediction percentage."""
    if prediction > 90:
        return "Fantastic! You're on track for excellent academic success. Keep up the great work and maintain your momentum."
    elif 70 <= prediction <= 90:
        return "You're doing well, but there's room for improvement. Focus on strengthening your study habits and leveraging available resources."
    elif 50 <= prediction < 70:
        return "Your success is promising, but you need to improve in key areas like time management and creating a more conducive study environment."
    else:
        return "Your academic performance may be at risk. Seek support from mentors, improve your study environment, and ensure access to essential resources."

@app.route("/", methods=["GET", "POST"])
def index():
    prediction = None
    message = None

    if request.method == "POST":
        print("POST request received!")  # Confirm POST request

        # Print the data coming from the form
        campus_residence = int(request.form["campus_residence"])
        convenience = int(request.form["convenience"])
        electricity_access = int(request.form["electricity_access"])
        water_access = int(request.form["water_access"])
        internet_access = int(request.form["internet_access"])
        study_environment = int(request.form["study_environment"])
        parental_support = int(request.form["parental_support"])
        peer_influence = int(request.form["peer_influence"])

        print(f"Form Data: {campus_residence}, {convenience}, {electricity_access}, {water_access}, {internet_access}, {study_environment}, {parental_support}, {peer_influence}")

        # Make prediction
        input_data = [[
            campus_residence, convenience, electricity_access,
            water_access, internet_access, study_environment,
            parental_support, peer_influence
        ]]

        prediction = model.predict(input_data)

        # Check prediction and print it for debugging
        print(f"Prediction Result: {prediction}")

        if prediction is not None and len(prediction) > 0:
            prediction = prediction[0] * 100  # Convert to percentage
            prediction = round(prediction, 2)
            message = generate_message(prediction)
        else:
            message = "Error: Unable to make a prediction. Please check your inputs or try again later."

    return render_template("index.html", prediction=prediction, message=message)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5004)
