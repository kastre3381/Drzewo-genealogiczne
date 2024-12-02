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
    return redirect("/")

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
        director = request.form['director']

        hour, minute = map(int, length.split(':'))
        length = datetime.time(hour=hour, minute=minute)

        print(length)

        database.addMovie(name=name, release_date=release_date, length=length, director=director)
        movies = database.getAllMovies()
        return render_template('movies.html', movies=movies)

    directors = database.getAllDirector()
    return render_template('create_movie.html', directors=directors)



@app.route('/user/all')
def users():
    persons = database.getAllUser()
    return render_template('users.html', persons=persons)

@app.route('/user/all/alive')
def users_alive():
    persons = database.getAllAliveUser()
    return render_template('users.html', persons=persons)

@app.route('/user/all/dead')
def users_dead():
    persons = database.getAllDeadUser()
    return render_template('users.html', persons=persons)

@app.route('/user/all/delete')
def users_delete_all():
    database.deleteAllUser()
    return redirect("/")

@app.route('/user/all/delete/dead')
def users_delete_all_dead():
    database.deleteDeadUser()
    return redirect("/")

@app.route('/user/<email>', methods=['GET'])
def get_user_by_email(email):
    user = database.getUserByEmail(email)
    return render_template('user_detail.html', user=user)

@app.route('/user/<email>/delete')
def delete_user_by_email(email):
    database.deleteUser(email)
    return redirect("/")

@app.route('/user/<email>/addRating', methods=['GET', 'POST'])
def add_comment_by_user(email):
    if request.method == 'POST':
        rating = request.form['rating']
        movie = request.form['movie']
        text = request.form['text']
        
        database.addComment(email, movie, rating, text)
        
        user = database.getUserByEmail(email)
        return render_template('user_detail.html', user=user)


    movies = database.getAllMovies()
    return render_template('create_comment.html', email=email, movies=movies)

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
            
        if deathdate and deathdate >= birthdate:  
            database.addUser(name, surname, birthdate, deathdate, gender, email)
        
        users = database.getAllUser()
        return render_template('users.html', persons=users, val="All")

    
    return render_template('create_user.html')




@app.route('/director/all')
def directors():
    persons = database.getAllDirector()
    val = "All"
    return render_template('directors.html', persons=persons, val=val)

@app.route('/director/all/alive')
def directors_alive():
    persons = database.getAllAliveDirector()
    val = "Alive"
    return render_template('directors.html', persons=persons, val=val)

@app.route('/director/all/dead')
def directors_dead():
    persons = database.getAllDeadDirector()
    val = "Dead"
    return render_template('directors.html', persons=persons, val=val)

@app.route('/director/all/delete')
def directors_delete_all():
    database.deleteAllDirector()
    return redirect("/")

@app.route('/director/all/delete/dead')
def directors_delete_all_dead():
    database.deleteDeadDirector()
    return redirect("/")

@app.route('/director/<email>', methods=['GET'])
def get_director_by_email(email):
    director = database.getDirectorByEmail(email)
    movies = database.getMoviesDirectedBy(email)
    if not movies:
        movies = {}
    return render_template('director_detail.html', director=director, movies=movies)


@app.route('/director/<email>/delete')
def delete_director_by_email(email):
    database.deleteDirector(email)
    return redirect("/")

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
            
        database.addDirector(name, surname, birthdate, deathdate, gender, email)
        directors = database.getAllDirector()
        val="All"
        return render_template('directors.html', persons=directors, val=val)

    
    return render_template('create_director.html')





@app.route("/user/all/addMultiple")
def addMultipleUsers():
    database.addUser("Michal", "Tracz", datetime.date(2002, 6, 17), None, "Male", "michTracz@gmail.com")
    database.addUser("Anna", "Nowak", datetime.date(1990, 4, 25), None, "Female", "anna.nowak@gmail.com")
    database.addUser("Jan", "Kowalski", datetime.date(1985, 12, 15), None, "Male", "jan.kowalski@gmail.com")
    database.addUser("Ewa", "Kaczmarek", datetime.date(1995, 8, 10), datetime.date(2020, 11, 1), "Female", "ewa.kaczmarek@gmail.com")
    database.addUser("Piotr", "Wójcik", datetime.date(1980, 3, 22), None, "Male", "piotr.wojcik@gmail.com")
    database.addUser("Zofia", "Lewandowska", datetime.date(1987, 11, 5), None, "Female", "zofia.lewandowska@gmail.com")
    database.addUser("Tomasz", "Zieliński", datetime.date(1992, 1, 30), None, "Male", "tomasz.zielinski@gmail.com")
    database.addUser("Karolina", "Szymańska", datetime.date(1996, 7, 18), None, "Female", "karolina.szymanska@gmail.com")
    database.addUser("Michał", "Wiśniewski", datetime.date(1982, 9, 5), datetime.date(2015, 8, 20), "Male", "michal.wisniewski@gmail.com")
    database.addUser("Magdalena", "Wróblewska", datetime.date(1990, 6, 3), None, "Female", "magdalena.wroblewska@gmail.com")
    database.addUser("Kamil", "Krzak", datetime.date(2000, 4, 17), None, "Male", "kamil.krzak@gmail.com")
    database.addUser("Daria", "Jankowska", datetime.date(1993, 5, 12), None, "Female", "daria.jankowska@gmail.com")
    database.addUser("Paweł", "Piotrowski", datetime.date(1988, 2, 2), None, "Male", "pawel.piotrowski@gmail.com")
    database.addUser("Monika", "Krawczyk", datetime.date(1997, 10, 20), None, "Female", "monika.krawczyk@gmail.com")
    database.addUser("Łukasz", "Adamczak", datetime.date(1991, 12, 4), None, "Male", "lukasz.adamczak@gmail.com")
    database.addUser("Olga", "Mazurek", datetime.date(1999, 1, 15), None, "Female", "olga.mazurek@gmail.com")
    database.addUser("Andrzej", "Grabowski", datetime.date(1983, 3, 25), None, "Male", "andrzej.grabowski@gmail.com")
    database.addUser("Katarzyna", "Pawlak", datetime.date(1994, 5, 28), None, "Female", "katarzyna.pawlak@gmail.com")
    database.addUser("Rafał", "Bąk", datetime.date(2001, 6, 15), None, "Male", "rafal.bak@gmail.com")
    database.addUser("Dorota", "Mikulska", datetime.date(1998, 11, 7), None, "Female", "dorota.mikulska@gmail.com")
    database.addUser("Jakub", "Kwiatkowski", datetime.date(1994, 2, 22), None, "Male", "jakub.kwiatkowski@gmail.com")
    database.addUser("Paulina", "Milewska", datetime.date(1996, 7, 30), None, "Female", "paulina.milewska@gmail.com")
    database.addUser("Marek", "Walentowicz", datetime.date(1988, 8, 14), None, "Male", "marek.walentowicz@gmail.com")
    database.addUser("Agata", "Kozłowska", datetime.date(1997, 1, 10), None, "Female", "agata.kozlowska@gmail.com")
    database.addUser("Artur", "Piątek", datetime.date(1992, 9, 16), None, "Male", "artur.piatek@gmail.com")
    database.addUser("Barbara", "Zawisza", datetime.date(1990, 4, 19), None, "Female", "barbara.zawisza@gmail.com")
    database.addUser("Szymon", "Borkowski", datetime.date(1993, 5, 4), None, "Male", "szymon.borkowski@gmail.com")
    database.addUser("Marta", "Jóźwiak", datetime.date(1989, 3, 13), None, "Female", "marta.joziak@gmail.com")
    database.addUser("Piotr", "Szewczyk", datetime.date(1995, 8, 30), None, "Male", "piotr.szewczyk@gmail.com")
    database.addUser("Karolina", "Zawisza", datetime.date(1985, 12, 2), None, "Female", "karolina.zawisza@gmail.com")
    database.addUser("Tomasz", "Wróblewski", datetime.date(1998, 6, 5), datetime.date(2010, 7, 19), "Male", "tomasz.wroblewski@gmail.com")
    database.addUser("Anna", "Wachowiak", datetime.date(1994, 2, 10), None, "Female", "anna.wachowiak@gmail.com")
    database.addUser("Jacek", "Czerwiński", datetime.date(1980, 3, 25), None, "Male", "jacek.czerwinski@gmail.com")
    database.addUser("Sylwia", "Tomaszewska", datetime.date(1982, 10, 18), None, "Female", "sylwia.tomaszewska@gmail.com")
    database.addUser("Patryk", "Pawlak", datetime.date(2000, 5, 14), None, "Male", "patryk.pawlak@gmail.com")
    database.addUser("Monika", "Wilk", datetime.date(1997, 4, 11), None, "Female", "monika.wilk@gmail.com")
    database.addUser("Marcin", "Borkowski", datetime.date(1996, 8, 20), None, "Male", "marcin.borkowski@gmail.com")
    database.addUser("Kinga", "Mazur", datetime.date(1993, 1, 30), None, "Female", "kinga.mazur@gmail.com")
    database.addUser("Sebastian", "Kaczmarek", datetime.date(1989, 6, 5), None, "Male", "sebastian.kaczmarek@gmail.com")
    database.addUser("Agnieszka", "Stolarz", datetime.date(1991, 12, 22), None, "Female", "agnieszka.stolarz@gmail.com")
    database.addUser("Jakub", "Kowal", datetime.date(1999, 3, 7), None, "Male", "jakub.kowal@gmail.com")
    database.addUser("Katarzyna", "Duda", datetime.date(1986, 7, 18), None, "Female", "katarzyna.duda@gmail.com")
    database.addUser("Piotr", "Zawisza", datetime.date(1994, 4, 12), None, "Male", "piotr.zawisza@gmail.com")
    database.addUser("Joanna", "Marek", datetime.date(1992, 10, 22), None, "Female", "joanna.marek@gmail.com")
    database.addUser("Radosław", "Wojda", datetime.date(1984, 12, 9), None, "Male", "radoslaw.wojda@gmail.com")
    database.addUser("Diana", "Górska", datetime.date(1999, 2, 3), None, "Female", "diana.gorska@gmail.com")
    database.addUser("Michał", "Markowski", datetime.date(1995, 9, 11), None, "Male", "michal.markowski@gmail.com")
    database.addUser("Ewa", "Marek", datetime.date(1992, 4, 25), None, "Female", "ewa.marek@gmail.com")
    database.addUser("Adam", "Stolarz", datetime.date(1985, 11, 10), None, "Male", "adam.stolarz@gmail.com")
    database.addUser("Joanna", "Piotrowska", datetime.date(1996, 8, 14), None, "Female", "joanna.piotrowska@gmail.com")
    database.addUser("Piotr", "Makowski", datetime.date(1998, 10, 20), None, "Male", "piotr.makowski@gmail.com")
    database.addUser("Aleksandra", "Sadowska", datetime.date(1994, 6, 7), None, "Female", "aleksandra.sadowska@gmail.com")
    database.addUser("Michał", "Wolak", datetime.date(1999, 9, 2), None, "Male", "michal.wolak@gmail.com")
    database.addUser("Wiktoria", "Wójcik", datetime.date(1992, 11, 16), None, "Female", "wiktoria.wojcik@gmail.com")
    database.addUser("Krzysztof", "Sienkiewicz", datetime.date(1989, 8, 29), None, "Male", "krzysztof.sienkiewicz@gmail.com")
    database.addUser("Elżbieta", "Nowak", datetime.date(1995, 3, 18), None, "Female", "elzbieta.nowak@gmail.com")
    database.addUser("Sebastian", "Milewski", datetime.date(1980, 6, 24), None, "Male", "sebastian.milewski@gmail.com")
    database.addUser("Sylwia", "Wielkopolska", datetime.date(1990, 5, 30), None, "Female", "sylwia.wielkopolska@gmail.com")
    database.addUser("Marek", "Borowski", datetime.date(1988, 7, 2), None, "Male", "marek.borowski@gmail.com")

    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)
