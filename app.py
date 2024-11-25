from flask import Flask, render_template, redirect, request
import database 
import datetime

app = Flask(__name__)

database = database.Database()


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/movie/all')
def movies():
    movies = database.getAllMovies()
    return render_template('movies.html', movies=movies)

@app.route('/movie/<name>', methods=['GET'])
def get_movie_by_name(name):
    movie = database.getMovieByName(name)
    director = database.getDirectorOfMovie(name)
    return render_template('movie_details.html', movie=movie, director=director)

@app.route('/movie/<name>/delete')
def delete_movie_by_name(name):
    database.deleteMovie(name)
    return render_template('index.html')

@app.route('/movie/<name>/assign_director', methods=['GET', 'POST'])
def assign_director(name):
    if request.method == 'POST':
        email = request.form['email']
        
        database.assignDirectorToMovie(email, name)
        movies = database.getAllMovies()
        return render_template('movies.html', movies=movies)
    
    directors = database.getAllPeople("Director")
    return render_template('assign_director.html', directors=directors, name=name)

@app.route('/movie/create_movie', methods=['GET', 'POST'])
def create_movie():
    if request.method == 'POST':
        name = request.form['name']
        release_date = request.form['release_date']
        release_date = datetime.datetime.strptime(release_date, "%Y-%m-%d").date()
        length = request.form['length']
        

        hour, minute = map(int, length.split(':'))
        length = datetime.time(hour=hour, minute=minute)

        print(length)

        database.addMovie(name=name, release_date=release_date, length=length)
        movies = database.getAllMovies()
        return render_template('movies.html', movies=movies)

    
    return render_template('create_movie.html')



@app.route('/user/all')
def users():
    persons = database.getAllPeople("User")
    return render_template('users.html', persons=persons)

@app.route('/user/all/alive')
def users_alive():
    persons = database.getAllAlivePeople("User")
    return render_template('users.html', persons=persons)

@app.route('/user/all/dead')
def users_dead():
    persons = database.getAllDeadPeople("User")
    return render_template('users.html', persons=persons)

@app.route('/user/all/delete')
def users_delete_all():
    database.deleteAllPerson("User")
    return render_template('index.html')

@app.route('/user/all/delete/dead')
def users_delete_all_dead():
    database.deleteDeadPerson("User")
    return render_template('index.html')

@app.route('/user/<email>', methods=['GET'])
def get_user_by_email(email):
    user = database.getPersonByEmail(email, "User")
    return render_template('user_detail.html', user=user)

@app.route('/user/<email>/delete')
def delete_user_by_email(email):
    database.deletePerson(email, "User")
    return render_template('index.html')

@app.route('/user/create_user', methods=['GET', 'POST'])
def create_user():
    if request.method == 'POST':
        name = request.form['name']
        surname = request.form['surname']
        birthdate = request.form['birthdate']
        deathdate = request.form['deathdate'] if request.form['deathdate'] else None
        gender = request.form['gender']
        email = request.form['email']
        birthdate = datetime.datetime.strptime(birthdate, "%Y-%m-%d").date()
        
        if deathdate:
            deathdate = datetime.datetime.strptime(deathdate, "%Y-%m-%d").date()
        else:
            deathdate = None
            
        database.addPerson(name, surname, birthdate, deathdate, gender, email, "User")
        users = database.getAllPeople("User")
        return render_template('people.html', persons=users)

    
    return render_template('create_person.html')




@app.route('/director/all')
def directors():
    persons = database.getAllPeople("Director")
    return render_template('directors.html', persons=persons)

@app.route('/director/all/alive')
def directors_alive():
    persons = database.getAllAlivePeople("Director")
    return render_template('directors.html', persons=persons)

@app.route('/director/all/dead')
def directors_dead():
    persons = database.getAllDeadPeople("Director")
    return render_template('directors.html', persons=persons)

@app.route('/director/all/delete')
def directors_delete_all():
    database.deleteAllPerson("Director")
    return render_template('index.html')

@app.route('/director/all/delete/dead')
def directors_delete_all_dead():
    database.deleteDeadPerson("Director")
    return render_template('index.html')

@app.route('/director/<email>', methods=['GET'])
def get_director_by_email(email):
    director = database.getPersonByEmail(email, "Director")
    return render_template('director_detail.html', director=director)

@app.route('/director/<email>/delete')
def delete_director_by_email(email):
    database.deletePerson(email, "Director")
    return render_template('index.html')

@app.route('/director/create_director', methods=['GET', 'POST'])
def create_director():
    if request.method == 'POST':
        name = request.form['name']
        surname = request.form['surname']
        birthdate = request.form['birthdate']
        deathdate = request.form['deathdate'] if request.form['deathdate'] else None
        gender = request.form['gender']
        email = request.form['email']
        birthdate = datetime.datetime.strptime(birthdate, "%Y-%m-%d").date()
        
        if deathdate:
            deathdate = datetime.datetime.strptime(deathdate, "%Y-%m-%d").date()
        else:
            deathdate = None
            
        database.addPerson(name, surname, birthdate, deathdate, gender, email, "Director")
        directors = database.getAllPeople("Director")
        return render_template('directors.html', persons=directors)

    
    return render_template('create_director.html')





@app.route("/user/all/addMultiple")
def addMultipleUsers():
    database.addPerson("Michal", "Tracz", datetime.date(2002, 6, 17), None, "Male", "michTracz@gmail.com", "User")
    database.addPerson("Anna", "Nowak", datetime.date(1990, 4, 25), None, "Female", "anna.nowak@gmail.com", "User")
    database.addPerson("Jan", "Kowalski", datetime.date(1985, 12, 15), None, "Male", "jan.kowalski@gmail.com", "User")
    database.addPerson("Ewa", "Kaczmarek", datetime.date(1995, 8, 10), datetime.date(2020, 11, 1), "Female", "ewa.kaczmarek@gmail.com", "User")
    database.addPerson("Piotr", "Wójcik", datetime.date(1980, 3, 22), None, "Male", "piotr.wojcik@gmail.com", "User")
    database.addPerson("Zofia", "Lewandowska", datetime.date(1987, 11, 5), None, "Female", "zofia.lewandowska@gmail.com", "User")
    database.addPerson("Tomasz", "Zieliński", datetime.date(1992, 1, 30), None, "Male", "tomasz.zielinski@gmail.com", "User")
    database.addPerson("Karolina", "Szymańska", datetime.date(1996, 7, 18), None, "Female", "karolina.szymanska@gmail.com", "User")
    database.addPerson("Michał", "Wiśniewski", datetime.date(1982, 9, 5), datetime.date(2015, 8, 20), "Male", "michal.wisniewski@gmail.com", "User")
    database.addPerson("Magdalena", "Wróblewska", datetime.date(1990, 6, 3), None, "Female", "magdalena.wroblewska@gmail.com", "User")
    database.addPerson("Kamil", "Krzak", datetime.date(2000, 4, 17), None, "Male", "kamil.krzak@gmail.com", "User")
    database.addPerson("Daria", "Jankowska", datetime.date(1993, 5, 12), None, "Female", "daria.jankowska@gmail.com", "User")
    database.addPerson("Paweł", "Piotrowski", datetime.date(1988, 2, 2), None, "Male", "pawel.piotrowski@gmail.com", "User")
    database.addPerson("Monika", "Krawczyk", datetime.date(1997, 10, 20), None, "Female", "monika.krawczyk@gmail.com", "User")
    database.addPerson("Łukasz", "Adamczak", datetime.date(1991, 12, 4), None, "Male", "lukasz.adamczak@gmail.com", "User")
    database.addPerson("Olga", "Mazurek", datetime.date(1999, 1, 15), None, "Female", "olga.mazurek@gmail.com", "User")
    database.addPerson("Andrzej", "Grabowski", datetime.date(1983, 3, 25), None, "Male", "andrzej.grabowski@gmail.com", "User")
    database.addPerson("Katarzyna", "Pawlak", datetime.date(1994, 5, 28), None, "Female", "katarzyna.pawlak@gmail.com", "User")
    database.addPerson("Rafał", "Bąk", datetime.date(2001, 6, 15), None, "Male", "rafal.bak@gmail.com", "User")
    database.addPerson("Dorota", "Mikulska", datetime.date(1998, 11, 7), None, "Female", "dorota.mikulska@gmail.com", "User")
    database.addPerson("Jakub", "Kwiatkowski", datetime.date(1994, 2, 22), None, "Male", "jakub.kwiatkowski@gmail.com", "User")
    database.addPerson("Paulina", "Milewska", datetime.date(1996, 7, 30), None, "Female", "paulina.milewska@gmail.com", "User")
    database.addPerson("Marek", "Walentowicz", datetime.date(1988, 8, 14), None, "Male", "marek.walentowicz@gmail.com", "User")
    database.addPerson("Agata", "Kozłowska", datetime.date(1997, 1, 10), None, "Female", "agata.kozlowska@gmail.com", "User")
    database.addPerson("Artur", "Piątek", datetime.date(1992, 9, 16), None, "Male", "artur.piatek@gmail.com", "User")
    database.addPerson("Barbara", "Zawisza", datetime.date(1990, 4, 19), None, "Female", "barbara.zawisza@gmail.com", "User")
    database.addPerson("Szymon", "Borkowski", datetime.date(1993, 5, 4), None, "Male", "szymon.borkowski@gmail.com", "User")
    database.addPerson("Marta", "Jóźwiak", datetime.date(1989, 3, 13), None, "Female", "marta.joziak@gmail.com", "User")
    database.addPerson("Piotr", "Szewczyk", datetime.date(1995, 8, 30), None, "Male", "piotr.szewczyk@gmail.com", "User")
    database.addPerson("Karolina", "Zawisza", datetime.date(1985, 12, 2), None, "Female", "karolina.zawisza@gmail.com", "User")
    database.addPerson("Tomasz", "Wróblewski", datetime.date(1998, 6, 5), datetime.date(2010, 7, 19), "Male", "tomasz.wroblewski@gmail.com", "User")
    database.addPerson("Anna", "Wachowiak", datetime.date(1994, 2, 10), None, "Female", "anna.wachowiak@gmail.com", "User")
    database.addPerson("Jacek", "Czerwiński", datetime.date(1980, 3, 25), None, "Male", "jacek.czerwinski@gmail.com", "User")
    database.addPerson("Sylwia", "Tomaszewska", datetime.date(1982, 10, 18), None, "Female", "sylwia.tomaszewska@gmail.com", "User")
    database.addPerson("Patryk", "Pawlak", datetime.date(2000, 5, 14), None, "Male", "patryk.pawlak@gmail.com", "User")
    database.addPerson("Monika", "Wilk", datetime.date(1997, 4, 11), None, "Female", "monika.wilk@gmail.com", "User")
    database.addPerson("Marcin", "Borkowski", datetime.date(1996, 8, 20), None, "Male", "marcin.borkowski@gmail.com", "User")
    database.addPerson("Kinga", "Mazur", datetime.date(1993, 1, 30), None, "Female", "kinga.mazur@gmail.com", "User")
    database.addPerson("Sebastian", "Kaczmarek", datetime.date(1989, 6, 5), None, "Male", "sebastian.kaczmarek@gmail.com", "User")
    database.addPerson("Agnieszka", "Stolarz", datetime.date(1991, 12, 22), None, "Female", "agnieszka.stolarz@gmail.com", "User")
    database.addPerson("Jakub", "Kowal", datetime.date(1999, 3, 7), None, "Male", "jakub.kowal@gmail.com", "User")
    database.addPerson("Katarzyna", "Duda", datetime.date(1986, 7, 18), None, "Female", "katarzyna.duda@gmail.com", "User")
    database.addPerson("Piotr", "Zawisza", datetime.date(1994, 4, 12), None, "Male", "piotr.zawisza@gmail.com", "User")
    database.addPerson("Joanna", "Marek", datetime.date(1992, 10, 22), None, "Female", "joanna.marek@gmail.com", "User")
    database.addPerson("Radosław", "Wojda", datetime.date(1984, 12, 9), None, "Male", "radoslaw.wojda@gmail.com", "User")
    database.addPerson("Diana", "Górska", datetime.date(1999, 2, 3), None, "Female", "diana.gorska@gmail.com", "User")
    database.addPerson("Michał", "Markowski", datetime.date(1995, 9, 11), None, "Male", "michal.markowski@gmail.com", "User")
    database.addPerson("Ewa", "Marek", datetime.date(1992, 4, 25), None, "Female", "ewa.marek@gmail.com", "User")
    database.addPerson("Adam", "Stolarz", datetime.date(1985, 11, 10), None, "Male", "adam.stolarz@gmail.com", "User")
    database.addPerson("Joanna", "Piotrowska", datetime.date(1996, 8, 14), None, "Female", "joanna.piotrowska@gmail.com", "User")
    database.addPerson("Piotr", "Makowski", datetime.date(1998, 10, 20), None, "Male", "piotr.makowski@gmail.com", "User")
    database.addPerson("Aleksandra", "Sadowska", datetime.date(1994, 6, 7), None, "Female", "aleksandra.sadowska@gmail.com", "User")
    database.addPerson("Michał", "Wolak", datetime.date(1999, 9, 2), None, "Male", "michal.wolak@gmail.com", "User")
    database.addPerson("Wiktoria", "Wójcik", datetime.date(1992, 11, 16), None, "Female", "wiktoria.wojcik@gmail.com", "User")
    database.addPerson("Krzysztof", "Sienkiewicz", datetime.date(1989, 8, 29), None, "Male", "krzysztof.sienkiewicz@gmail.com", "User")
    database.addPerson("Elżbieta", "Nowak", datetime.date(1995, 3, 18), None, "Female", "elzbieta.nowak@gmail.com", "User")
    database.addPerson("Sebastian", "Milewski", datetime.date(1980, 6, 24), None, "Male", "sebastian.milewski@gmail.com", "User")
    database.addPerson("Sylwia", "Wielkopolska", datetime.date(1990, 5, 30), None, "Female", "sylwia.wielkopolska@gmail.com", "User")
    database.addPerson("Marek", "Borowski", datetime.date(1988, 7, 2), None, "Male", "marek.borowski@gmail.com", "User")

    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
