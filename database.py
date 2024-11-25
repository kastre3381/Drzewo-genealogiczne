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
            
            
    def addPerson(self, name, surname, birthdate, deathdate, gender, email, label : str):
        query_create = """
        CREATE (p:Person:
        """ + label + """ 
        {name: $name, surname: $surname, birthdate: $birthdate, deathdate: $deathdate, gender: $gender, email: $email})
        RETURN p
        """

        with self.driver.session() as session:
            session.run(query_create, name=name, 
                        surname=surname, birthdate=birthdate, 
                        deathdate=deathdate, gender=gender,
                        email=email)


    def deletePerson(self, email, label):
        query_delete = """
        MATCH (p:Person:
        """ + label + """ 
        {email: $email})
        DELETE p
        """
        
        with self.driver.session() as session:
            session.run(query_delete, email=email)
            
    def deleteDeadPerson(self, label):
        query_delete = """
        MATCH (p:Person:
        """ + label + """)
        WHERE p.deathdate IS NOT NULL
        DELETE p
        """

        with self.driver.session() as session:
            session.run(query_delete)

    def deleteAllPerson(self, label : str):
        query_delete = """
        MATCH (m:Person:
        """ + label + """) 
        DELETE m
        """

        with self.driver.session() as session:
            session.run(query_delete)

    def getAllPeople(self, label : str):
        query = """
        MATCH (p:Person:
        """ + label + """)
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
        
    def getAllAlivePeople(self, label : str):
        query = """
        MATCH (p:Person:
        """ + label + """)
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
        
    def getAllDeadPeople(self, label : str):
        query = """
        MATCH (p:Person:
        """ + label + """)
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
    
    
    def getPersonByEmail(self, email, label : str):
        query = """
        MATCH (u:Person:
        """ + label + """) 
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
        MATCH (p:Person:Director {email: $director_email}), (m:Movie {name: $movie_name})
        CREATE (p)-[:DIRECTED]->(m)
        RETURN p, m
        """
        with self.driver.session() as session:
            session.run(query_create_directed, director_email=director_email, movie_name=movie_name)
            
            query_create_directed_by = """
            MATCH (p:Person:Director {email: $director_email}), (m:Movie {name: $movie_name})
            CREATE (p)<-[:DIRECTED_BY]-(m)
            RETURN p, m
            """ 
            
            session.run(query_create_directed_by, director_email=director_email, movie_name=movie_name)
            
    def getDirectorOfMovie(self, movie_name: str):
        query = """
        MATCH (m:Movie {name: $movie_name})-[:DIRECTED_BY]->(d:Person:Director)
        RETURN d.name as name, d.surname as surname, d.email as email
        """

        with self.driver.session() as session:
            result = session.run(query, movie_name=movie_name)
            director = result.single()

            if director:
                return director
            else:
                return None
    