from neo4j import GraphDatabase
from neo4j.time import Time
import datetime

class Database:
    def __init__(self):
        self.NEO4J_URI="neo4j+s://b4c84343.databases.neo4j.io"
        self.NEO4J_USERNAME="neo4j"
        self.NEO4J_PASSWORD="8F28a6wBRxlyyw747-qAqw4zqGThFydPEihtBJnGQ58"
        self.AURA_INSTANCEID="b4c84343"
        self.AURA_INSTANCENAME="Instance01"
        self.driver = GraphDatabase.driver(self.NEO4J_URI, auth=(self.NEO4J_USERNAME, self.NEO4J_PASSWORD))
        
    def close(self):
        self.driver.close()
        
    def addMovie(self, name : str, release_date : datetime, length : datetime.time, director : str):
       query_check = """
        MATCH (m:Movie {name: $name})
        RETURN m
        """

       with self.driver.session() as session:
           result_check = session.run(query_check, name=name)
           existing_movie = result_check.single()
           if existing_movie:
                return 
           
           query = """
           CREATE (m:Movie {name: $name, release_date: $release_date, length: $length})
           RETURN m
           """
           
           session.run(query, name=name, release_date=release_date, length=length)
           
           query = """
           MATCH (m:Movie {name: $name}), (d:Director {email: $director})
           CREATE (d)-[:DIRECTED]->(m)
           RETURN m, d
           """
           session.run(query, name=name, director=director)
        
    def deleteMovies(self):
        query = """
        MATCH (m:Movie)-[r]-()
        DETACH DELETE r, m
        """

        with self.driver.session() as session:
            session.run(query)

        
    def getAllMovies(self):
        query = """
        MATCH (m:Movie)
        RETURN m.name AS name, m.release_date AS release_date, m.length AS length
        """
        
        with self.driver.session() as session:
            result = session.run(query)
            movies = []
            for record in result:
                if isinstance(record['length'], Time):
                    neo4j_time = record['length']
                    length = datetime.time(neo4j_time.hour, neo4j_time.minute)
                    formatted_length = length.strftime('%H:%M')  # Teraz możemy użyć strftime
                else:
                    formatted_length = None
                movie = {
                    "name": record["name"],
                    "release_date": record["release_date"],
                    "length": formatted_length
                }
                movies.append(movie)
                
            return movies
        
    def getMovieByName(self, name):
        query = """
        MATCH (m:Movie)
        WHERE m.name = $name
        RETURN m.name AS name, m.release_date AS release_date, m.length AS length
        """
        with self.driver.session() as session:
            result = session.run(query, name=name)
            movie = result.single()
            if movie:
                # Sprawdzenie, czy 'length' to obiekt neo4j.time.Time
                if isinstance(movie['length'], Time):
                    neo4j_time = movie['length']
                    # Konwersja na datetime.time
                    length = datetime.time(neo4j_time.hour, neo4j_time.minute)
                    formatted_length = length.strftime('%H:%M')  # Formatowanie czasu na HH:MM
                else:
                    formatted_length = None

                # Zwrócenie danych filmu z przekształconym czasem
                return {
                    'name': movie['name'],
                    'release_date': movie['release_date'],
                    'length': formatted_length
                }
            else:
                return None
        
    def deleteMovie(self, name):
        query = """
        MATCH (m:Movie {name: $name})-[r]-()
        DETACH DELETE r, m
        """

        with self.driver.session() as session:
            try:
                session.run(query, name=name)
                print(f"Film '{name}' i jego relacje zostały usunięte.")
            except Exception as e:
                print(f"Error during deleting movie: {e}")

            
    def addUser(self, name, surname, birthdate, deathdate, gender, email):
        query_check = """
        MATCH (m:User {email: $email})
        RETURN m
        """

        with self.driver.session() as session:
            result_check = session.run(query_check, email=email)
            existing_person = result_check.single()
            
            if existing_person:
                print(f"User with email {email} already exists.")
                return 
           
            query_create = """
            CREATE (p:User {name: $name, surname: $surname, birthdate: $birthdate, deathdate: $deathdate, gender: $gender, email: $email})
            RETURN p
            """
            session.run(query_create, name=name, 
                        surname=surname, birthdate=birthdate, 
                        deathdate=deathdate, gender=gender,
                        email=email)

    def addDirector(self, name, surname, birthdate, deathdate, gender, email):
        query_check = """
        MATCH (m:Director {email: $email})
        RETURN m
        """

        with self.driver.session() as session:
            result_check = session.run(query_check, email=email)
            existing_person = result_check.single()
            
            if existing_person:
                print(f"Director with email {email} already exists.")
                return 
           
            query_create = """
            CREATE (p:Director {name: $name, surname: $surname, birthdate: $birthdate, deathdate: $deathdate, gender: $gender, email: $email})
            RETURN p
            """
            session.run(query_create, name=name, 
                        surname=surname, birthdate=birthdate, 
                        deathdate=deathdate, gender=gender,
                        email=email)


    def deleteUser(self, email):
        query_delete = """
        MATCH (u:User {email: $email})
        OPTIONAL MATCH (u)-[:COMMENTED]->(c:Comment)-[:COMMENTED_UNDER]->(m:Movie)
        DETACH DELETE u, c
        """
        
        with self.driver.session() as session:
            session.run(query_delete, email=email)
            
            
    def deleteDirector(self, email):
        query_check = """
        MATCH (p:Director {email: $email})
        RETURN p
        """
        
        with self.driver.session() as session:
            result = session.run(query_check, email=email)
            if result.single() is None:
                print("Director not found!")
                return
            
            # Jeśli reżyser istnieje, usuń go
            query_delete = """
            MATCH (p:Director {email: $email})
            OPTIONAL MATCH (p)-[r:DIRECTED]->(m:Movie)
            OPTIONAL MATCH (c:Comment)-[r2:COMMENTED_UNDER]->(m:Movie)
            DELETE r, r2, p, m, c
            """
            session.run(query_delete, email=email)
            print("Director deleted successfully.")
            
            
    def deleteDeadUser(self):
        query_delete = """
        MATCH (u:User)
        OPTIONAL MATCH (u)-[:COMMENTED]->(c:Comment)-[:COMMENTED_UNDER]->(m:Movie)
        WHERE u.deathdate IS NOT NULL
        DETACH DELETE u, c
        """

        with self.driver.session() as session:
            session.run(query_delete)
            
    def deleteDeadDirector(self):
        query_delete = """
        MATCH (p:Director)
        OPTIONAL MATCH (p)-[:DIRECTED]->(m:Movie)<-[:COMMENTED_UNDER]-(c:Comment)
        WHERE p.deathdate IN NOT NULL
        DETACH DELETE p, m, c
        """

        with self.driver.session() as session:
            session.run(query_delete)

    def deleteAllUser(self):
        query_delete = """
        MATCH (u:User)
        OPTIONAL MATCH (u)-[:COMMENTED]->(c:Comment)-[:COMMENTED_UNDER]->(m:Movie)
        DETACH DELETE u, c
        """

        with self.driver.session() as session:
            session.run(query_delete)
            
    def deleteAllDirector(self):
        query_delete = """
        MATCH (m:Director) 
        DELETE m
        """

        with self.driver.session() as session:
            session.run(query_delete)
    

    def getAllUser(self):
        query = """
        MATCH (p:User)
        RETURN p
        """
        with self.driver.session() as session:
            result = session.run(query)
            persons = []
            for record in result:
                person = record["p"]
                persons.append({
                    "name": person["name"],
                    "surname": person["surname"],
                    "birthdate": person.get("birthdate", ""),
                    "deathdate": person.get("deathdate", ""),
                    "gender": person.get("gender", ""),
                    "email": person.get("email", "")
                })
            return persons
        
    def getAllDirector(self):
        query = """
        MATCH (p:Director)
        RETURN p
        """
        with self.driver.session() as session:
            result = session.run(query)
            persons = []
            for record in result:
                person = record["p"]
                persons.append({
                    "name": person["name"],
                    "surname": person["surname"],
                    "birthdate": person.get("birthdate", ""),
                    "deathdate": person.get("deathdate", ""),
                    "gender": person.get("gender", ""),
                    "email": person.get("email", "")
                })
            return persons
        
    def getAllAliveUser(self):
        query = """
        MATCH (p:User)
        WHERE p.deathdate IS NULL
        RETURN p
        """
        with self.driver.session() as session:
            result = session.run(query)
            persons = []
            for record in result:
                person = record["p"]
                persons.append({
                    "name": person["name"],
                    "surname": person["surname"],
                    "birthdate": person.get("birthdate", ""),
                    "deathdate": person.get("deathdate", ""),
                    "gender": person.get("gender", ""),
                    "email": person.get("email", "")
                })
            return persons
        
    def getAllAliveDirector(self):
        query = """
        MATCH (p:Director)
        WHERE p.deathdate IS NULL
        RETURN p
        """
        with self.driver.session() as session:
            result = session.run(query)
            persons = []
            for record in result:
                person = record["p"]
                persons.append({
                    "name": person["name"],
                    "surname": person["surname"],
                    "birthdate": person.get("birthdate", ""),
                    "deathdate": person.get("deathdate", ""),
                    "gender": person.get("gender", ""),
                    "email": person.get("email", "")
                })
            return persons

    def getAllDeadUser(self):
        query = """
        MATCH (p:User)
        WHERE p.deathdate IS NOT NULL
        RETURN p
        """
        with self.driver.session() as session:
            result = session.run(query)
            persons = []
            for record in result:
                person = record["p"]
                persons.append({
                    "name": person["name"],
                    "surname": person["surname"],
                    "birthdate": person.get("birthdate", ""),
                    "deathdate": person.get("deathdate", ""),
                    "gender": person.get("gender", ""),
                    "email": person.get("email", "")
                })
            return persons
        
            
    def getAllDeadDirector(self):
        query = """
        MATCH (p:Director)
        WHERE p.deathdate IS NOT NULL
        RETURN p
        """
        with self.driver.session() as session:
            result = session.run(query)
            persons = []
            for record in result:
                person = record["p"]
                persons.append({
                    "name": person["name"],
                    "surname": person["surname"],
                    "birthdate": person.get("birthdate", ""),
                    "deathdate": person.get("deathdate", ""),
                    "gender": person.get("gender", ""),
                    "email": person.get("email", "")
                })
            return persons
    
    
    def getUserByEmail(self, email):
        query = """
        MATCH (u:User) 
        WHERE u.email = $email
        RETURN u
        """
        with self.driver.session() as session:
            result = session.run(query, email=email)
            user = result.single()
            if user:
                return user['u']
            else:
                return None
            
    def getDirectorByEmail(self, email):
        query = """
        MATCH (u:Director) 
        WHERE u.email = $email
        RETURN u
        """
        with self.driver.session() as session:
            result = session.run(query, email=email)
            user = result.single()
            if user:
                return user['u']
            else:
                return None        
    
    def assignDirectorToMovie(self, director_email, movie_name):
        query_create_directed = """
        MATCH (p:Director {email: $director_email}), (m:Movie {name: $movie_name})
        CREATE (p)-[:DIRECTED]->(m)
        RETURN p, m
        """
        with self.driver.session() as session:
            session.run(query_create_directed, director_email=director_email, movie_name=movie_name)
            
    def getDirectorOfMovie(self, movie_name: str):
        query = """
        MATCH (m:Movie {name: $movie_name})<-[:DIRECTED]-(d:Director)
        RETURN d.name as name, d.surname as surname, d.email as email
        """

        with self.driver.session() as session:
            result = session.run(query, movie_name=movie_name)
            director = result.single()

            if director:
                return director
            else:
                return None
            
    def getMoviesNotDirectedBy(self, director_email):
        query = """
        MATCH (d:Director {email: $director_email}), (m:Movie)
        WHERE NOT (d)-[:DIRECTED]->(m)
        RETURN m.name as name
        """

        with self.driver.session() as session:
            result = session.run(query, director_email=director_email)
            movies = []

            for record in result:
                movies.append(record["name"])

            return movies
            
    def getMoviesDirectedBy(self, director_email: str):
        query = """
        MATCH (d:Director {email: $director_email})-[:DIRECTED]->(m:Movie)
        RETURN m.name AS name, m.release_date AS release_date, m.length AS length
        """

        with self.driver.session() as session:
            result = session.run(query, director_email=director_email)
            movies = []

            for record in result:
                movies.append({"name": record["name"]})

            return movies if movies else None
        
    def addComment(self, email, name, rating, text):
        query = """
        MATCH (k:Key)
        RETURN k.current_key AS current_key
        """
        
        with self.driver.session() as session:
            current_key = session.run(query).single()['current_key']
            print(current_key)
            query = """
            CREATE (c:Comment {key: $key, rating: $rating, text: $text})
            RETURN c
            """
            session.run(query, key=current_key, rating=rating, text=text)

            query = """
            MATCH (u:User {email: $email}), (c:Comment {key: $key})
            CREATE (u)-[:COMMENTED]->(c)
            """
            session.run(query, key=current_key, email=email)

            query = """
            MATCH (c:Comment {key: $key}), (m:Movie {name: $name})
            CREATE (c)-[:COMMENTED_UNDER]->(m)
            """
            session.run(query, key=current_key, name=name)
            
            query = """
            MATCH(k:Key)
            SET k.current_key = k.current_key + 1
            """
            session.run(query)
            
        
    def getAllCommentsByUser(self, email):
        query = """
        MATCH (u:User {email: $email})-[:COMMENTED]->(c:Comment)
        WITH c
        MATCH (c)-[:COMMENTED_UNDER]->(m:Movie)
        RETURN c.key AS key, c.rating AS rating, c.text AS text, m.name AS name
        """
        num = 0
        with self.driver.session() as session:
            result = session.run(query, email=email)
            comments = []
            for record in result:
                num+=1
                comment = {
                    "name": record["name"],
                    "key": record["key"],
                    "rating": record["rating"],
                    "text": record["text"],
                }
                comments.append(comment)
            return comments, num
        
    def deleteComment(self, key):
        query = """
        MATCH (c:Comment {key: $key})
        OPTIONAL MATCH (c)-[r:COMMENTED]->(u:User)
        OPTIONAL MATCH (c)-[r2:COMMENTED_UNDER]->(m:Movie)
        DETACH DELETE c, r, r2
        """

        with self.driver.session() as session:
            try:
                result = session.run(query, key=key)
                print(f"Komentarz o kluczu {key} i jego relacje zostały usunięte.")
            except Exception as e:
                print(f"Error during deleting comment: {e}")

    def getMovieRating(self, name):
        query_avg = """
        MATCH (m:Movie {name: $name})<-[:COMMENTED_UNDER]-(c:Comment)
        RETURN c.rating AS rating
        """

        with self.driver.session() as session: 
            result_avg = session.run(query_avg, name=name)
            a, b = 0.0, 0.0
            
            for record in result_avg:
                b+=1
                a+=int(record["rating"])
                print("rec:",a)
                
            avg = float(a)/float(b) if b else 0.0
            

            return avg 

    def getDirectorRating(self, email):
        query_avg = """
        MATCH (m:Movie)<-[:COMMENTED_UNDER]-(c:Comment)
        WITH m, c
        MATCH (m)<-[:DIRECTED]-(d:Director {email: $email})
        RETURN c.rating AS rating
        """

        with self.driver.session() as session: 
            result_avg = session.run(query_avg, email=email)
            a, b = 0.0, 0.0
            
            for record in result_avg:
                b+=1
                a+=int(record["rating"])
                print("rec:",a)
                
            avg = float(a)/float(b) if b else 0.0
            

            return avg 




