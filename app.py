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
        # Gather inputs from the form
        campus_residence = int(request.form["campus_residence"])
        convenience = int(request.form["convenience"])
        electricity_access = int(request.form["electricity_access"])
        water_access = int(request.form["water_access"])
        internet_access = int(request.form["internet_access"])
        study_environment = int(request.form["study_environment"])
        parental_support = int(request.form["parental_support"])
        peer_influence = int(request.form["peer_influence"])

        # Make a prediction
        input_data = [[
            campus_residence, convenience, electricity_access,
            water_access, internet_access, study_environment,
            parental_support, peer_influence
        ]]
        prediction = model.predict(input_data)[0]
        
        # Generate a dynamic message
        message = generate_message(prediction * 100)

    return render_template("index.html", prediction=round(prediction, 2) * 100, message=message)


if __name__ == '__main__':
    app.run(port=4004)
