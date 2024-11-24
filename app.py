from flask import Flask, render_template, redirect, request
import database 
import datetime

app = Flask(__name__)

database = database.Database()


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/user/all')
def users():
    persons = database.getAllUsers()
    return render_template('user.html', persons=persons)

@app.route('/user/<email>', methods=['GET'])
def get_user_by_email(email):
    user = database.getUserByEmail(email)
    return render_template('user_detail.html', user=user)

@app.route('/user/create_user', methods=['GET', 'POST'])
def create_user():
    if request.method == 'POST':
        # Get form data
        name = request.form['name']
        surname = request.form['surname']
        birthdate = request.form['birthdate']
        deathdate = request.form['deathdate'] if request.form['deathdate'] else None
        gender = request.form['gender']
        email = request.form['email']

        # Convert birthdate to datetime object
        birthdate = datetime.datetime.strptime(birthdate, "%Y-%m-%d").date()
        
        # If deathdate exists, convert to datetime object
        if deathdate:
            deathdate = datetime.datetime.strptime(deathdate, "%Y-%m-%d").date()
        else:
            deathdate = None

        # Add person to the database
        database.addPerson(name, surname, birthdate, deathdate, gender, email, "User")

        # Redirect to a page showing all users after adding the new user
        users = database.getAllUsers()
        return render_template('user.html', persons=users)

    # For GET requests, render the form
    return render_template('create_user.html')



if __name__ == "__main__":
    app.run(debug=True)
