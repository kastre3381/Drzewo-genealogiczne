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
        
    def addMovie(self, name : str, release_date : datetime, director : str, length : datetime.time):
       query_check = """
        MATCH (m:Movie {name: $name})
        RETURN m
        """

       with self.driver.session() as session:
           result_check = session.run(query_check, name=name)
           existing_movie = result_check.single()
           if existing_movie:
                return f"Movie with the name '{name}' already exists."
           
           query = """
           CREATE (m:Movie {name: $name, release_date: $release_date, director: $director, length: $length})
           RETURN m
           """
           
           result = session.run(query, name=name, release_date=release_date, director=director, length=length)
           record = result.single()
           if record:
               return f"Movie '{record['m']['name']}' added successfully."
           else:
               return "Error adding movie."
        
        
    def getAllMovies(self):
        query = """
        MATCH (m:Movie)
        RETURN m.name AS name, m.release_date AS release_date, m.director AS director, m.length AS length
        """
        
        with self.driver.session() as session:
            result = session.run(query)
            movies = []
            for record in result:
                # Collect movie information from the result
                movie = {
                    "name": record["name"],
                    "release_date": record["release_date"],
                    "director": record["director"],
                    "length": record["length"]
                }
                movies.append(movie)
                
            return movies
        
        
    def deleteMovie(self, name):
        query_delete = """
        MATCH (m:Movie {name: $name})
        DELETE m
        """

        with self.driver.session() as session:
            result = session.run(query_delete, name=name)
            if result.summary().counters.nodes_deleted > 0:
                return f"Movie '{name}' has been deleted."
            else:
                return f"No movie found with the name '{name}'."
            
            
    def addPerson(self, name, surname, birthdate, deathdate, gender, email, label : str):
        query_create = """
        CREATE (p:Person:
        """ + label + """
        {name: $name, surname: $surname, birthdate: $birthdate, deathdate: $deathdate, gender: $gender, email: $email})
        RETURN p
        """

        with self.driver.session() as session:
            result_create = session.run(query_create, name=name, 
                                        surname=surname, birthdate=birthdate, 
                                        deathdate=deathdate, gender=gender,
                                        email=email)
            record = result_create.single()

            if record:
                return f"Person '{record['p']['name']}' added successfully."
            else:
                return "Error adding person."

    
    def deletePerson(self, name, surname, label):
        query_delete = """
        MATCH (p:Person:{label} {name: $name, surname: $surname})
        DELETE p
        """

        with self.driver.session() as session:
            result = session.run(query_delete, name=name, surname=surname)
            if result.summary().counters.nodes_deleted > 0:
                return f"Person '{name} {surname}' has been deleted."
            else:
                return f"No person found with the name '{name} {surname}'."

    def deletePerson(self, email, label):
        query_delete = """
        MATCH (p:Person:
        """ + label + """
        {email: $email})
        DELETE p
        """

        with self.driver.session() as session:
            result = session.run(query_delete, email=email)
            if result.summary().counters.nodes_deleted > 0:
                return f"Person '{email}' has been deleted."
            else:
                return f"No person found with the email '{email}'."

    def getAllUsers(self):
        query = """
        MATCH (p:Person:User)
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
    
    
    def deleteAllUsers(self):
        query_delete = """
        MATCH (m:Person:User)
        DELETE m
        """

        with self.driver.session() as session:
            session.run(query_delete)
    
    
    def getUserByEmail(self, email):
        query = """
        MATCH (u:Person:User)
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