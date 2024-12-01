from neo4j import GraphDatabase
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
        
    def addMovie(self, name : str, release_date : datetime, length : datetime.time):
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
        
        
    def getAllMovies(self):
        query = """
        MATCH (m:Movie)
        RETURN m.name AS name, m.release_date AS release_date, m.length AS length
        """
        
        with self.driver.session() as session:
            result = session.run(query)
            movies = []
            for record in result:
                movie = {
                    "name": record["name"],
                    "release_date": record["release_date"],
                    "length": record["length"]
                }
                movies.append(movie)
                
            return movies
        
    def getMovieByName(self, name):
        query = """
        MATCH (m:Movie)
        WHERE m.name = $name
        RETURN m
        """
        with self.driver.session() as session:
            result = session.run(query, name=name)
            movie = result.single()
            if movie:
                return movie['m']
            else:
                return None
        
    def deleteMovie(self, name):
        query_delete = """
        MATCH (m:Movie {name: $name})
        DELETE m
        """

        with self.driver.session() as session:
            session.run(query_delete, name=name)
            
            
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
            CREATE (p:User {name: $name, surname: $surname, birthdate: $birthdate, deathdate: $deathdate, gender: $gender, email: $email})
            RETURN p
            """
            session.run(query_create, name=name, 
                        surname=surname, birthdate=birthdate, 
                        deathdate=deathdate, gender=gender,
                        email=email)


    def deleteUser(self, email):
        query_delete = """
        MATCH (p:User {email: $email})
        DELETE p
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
            DELETE r, p
            """
            session.run(query_delete, email=email)
            print("Director deleted successfully.")
            
            
    def deleteDeadUser(self):
        query_delete = """
        MATCH (p:Person)
        WHERE p.deathdate IS NOT NULL
        DELETE p
        """

        with self.driver.session() as session:
            session.run(query_delete)
            
    def deleteDeadDirector(self):
        query_delete = """
        MATCH (p:Director)
        WHERE p.deathdate IS NOT NULL
        DELETE p
        """

        with self.driver.session() as session:
            session.run(query_delete)

    def deleteAllUser(self):
        query_delete = """
        MATCH (m:User) 
        DELETE m
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
        CREATE (p)-[:DIRECTED]->(m),
               (m)-[:DIRECTED_BY]->(p)
        RETURN p, m
        """
        with self.driver.session() as session:
            session.run(query_create_directed, director_email=director_email, movie_name=movie_name)
            
    def getDirectorOfMovie(self, movie_name: str):
        query = """
        MATCH (m:Movie {name: $movie_name})-[:DIRECTED_BY]->(d:Director)
        RETURN d.name as name, d.surname as surname, d.email as email
        """

        with self.driver.session() as session:
            result = session.run(query, movie_name=movie_name)
            director = result.single()

            if director:
                return director
            else:
                return None
            
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