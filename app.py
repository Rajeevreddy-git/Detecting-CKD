from flask import Flask, render_template, request, redirect, url_for, session                            # type: ignore
import pickle
from werkzeug.security import check_password_hash, generate_password_hash                                    # type: ignore

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Replace with a strong secret key

# Load the machine learning model
with open('model1.pkl', 'rb') as file:
    model = pickle.load(file)

# User data for authentication
users = {
    'admin': generate_password_hash('admin')  # Hashed password for admin
}

@app.route("/", methods=["GET", "POST"])
def home():
    return render_template('home.html')

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        if username == 'admin' and password == 'admin':  # Hardcoded admin credentials
            session['username'] = username
            return redirect(url_for('input_page'))
        else:
            return render_template('login.html', error='Invalid username or password')
    return render_template('login.html')

@app.route("/input", methods=["POST", "GET"])
def input_page():
    if 'username' not in session:
        return redirect(url_for('login'))  # Ensure user is logged in

    result = None
    if request.method == "POST":
        try:
            # Collect input from the form with validation
            age = request.form.get("Age")
            bp = request.form.get('Bp')
            sg = request.form.get('Sg')
            al = request.form.get('Al')
            bgr = request.form.get('Bgr')
            bu = request.form.get('Bu')
            sc = request.form.get('Sc')
            sod = request.form.get('Sod')
            pot = request.form.get('Pot')
            hemo = request.form.get('Hemo')
            pcv = request.form.get('Pcv')
            wc = request.form.get('Wc')
            rc = request.form.get('Rc')
            htn = request.form.get('Htn')

            # Check if any required fields are missing or invalid
            if not all([age, bp, sg, al, bgr, bu, sc, sod, pot, hemo, pcv, wc, rc, htn]):
                result = "Error: All fields are required."
            else:
                # Ensure valid number inputs before converting to float
                try:
                    age = float(age)
                    bp = float(bp)
                    sg = float(sg)
                    al = float(al)
                    bgr = float(bgr)
                    bu = float(bu)
                    sc = float(sc)
                    sod = float(sod)
                    pot = float(pot)
                    hemo = float(hemo)
                    pcv = float(pcv)
                    wc = float(wc)
                    rc = float(rc)
                    htn = int(htn)  # Hypertension is likely an integer

                    # Prepare the input for prediction
                    user_input = [[age, bp, sg, al, bgr, bu, sc, sod, pot, hemo, pcv, wc, rc, htn]]

                    # Make prediction using the model
                    prediction = model.predict(user_input)

                    # Display the result based on prediction (0 for CKD, 2 for No CKD)
                    if prediction[0] == 0:
                        result = "High Chance of Chronic Kidney Disease (CKD)"
                    elif prediction[0] == 2:
                        result = "Low Chance of Chronic Kidney Disease (No CKD)"
                    else:
                        result = "Invalid prediction value"

                except ValueError:
                    result = "Error: Please ensure all inputs are valid numbers."

        except Exception as e:
            result = f"Error: {str(e)}"

    return render_template("input.html", result=result)


@app.route("/logout")
def logout():
    session.pop('username', None)
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(port=5001, debug=True)
