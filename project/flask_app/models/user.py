from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

db="project"
class User:
    def __init__( self , data ):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password=data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM users;"

        results = connectToMySQL('project').query_db(query)

        users = []
        for x in results:
            users.append( cls(x) )
        return users 

    @classmethod
    def save(cls, data ):
        query = ''' INSERT INTO users ( first_name,last_name,email,password )
        VALUES ( %(first_name)s , %(last_name)s , %(email)s ,%(password)s);'''
        results= connectToMySQL('project').query_db( query, data )
        return results
    
    @classmethod
    def get_by_email(cls,data):
        query = "SELECT * FROM users WHERE email = %(email)s"
        results= connectToMySQL('project').query_db(query,data)
        if len(results) < 1:
            return False
        return cls(results[0])
    
    @classmethod
    def get_by_id(cls,data):
        query="SELECT * FROM users WHERE id=%(id)s"
        results=connectToMySQL('project').query_db( query, data )
        return cls(results[0])

    @classmethod
    def delete_user(cls,data):
        query=" DELETE FROM users WHERE id=%(id)s;"
        results=connectToMySQL('project').query_db(query,data)
        return results


    @staticmethod
    def validate_user(data):
        is_valid =True
        if len(data['first_name']) <= 1:
            flash("Name must be more than one character !!!")
            is_valid=False
        if len(data['last_name'])<= 1:
            flash("Last name must be more than one charachter!!!")
            is_valid=False
        if len(data['email']) == 0:
            flash('invalid email!!')
            is_valid=False
        if not EMAIL_REGEX.match(data['email']):
            flash("Invalid email/password address!")
            is_valid = False
        query = "SELECT * FROM users WHERE email=%(email)s"
        results= connectToMySQL('project').query_db(query,data)
        if len(results)!=0:
            flash('email is been used!')
            is_valid=False
        if len(data['password'])==0:
            flash("Enter correct email/password!!")
            is_valid=False


        return is_valid


