from flask_app.config.mysqlconnection import connectToMySQL
import pprint
from flask_app.models.hobby_model import Hobby
from flask import flash
import re 

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
PASWORD_REGEX = re.compile(r'^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-])$')


db = "hobby_dobby"

class User:
    def __init__(self,data):
        self.id = data['id']
        self.name = data['name']
        self.username = data['username']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.hobbies = []

    @classmethod
    def save(cls,data):
        query = "INSERT INTO users (name,username,email,password) VALUES (%(name)s, %(username)s, %(email)s, %(password)s)"
        return connectToMySQL(db).query_db(query,data)
    
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM users"
        results = connectToMySQL(db).query_db(query)
        all_users = []
        pprint.pprint(results)
        for user in results:
            all_users.append( cls(user))
        return all_users
    

    @classmethod
    def get_user_by_email(cls,data):
        query = "SELECT * FROM users WHERE email = %(email)s"
        results = connectToMySQL(db).query_db(query,data)
        if len(results) < 1:
            return False
        return cls(results[0])


    @classmethod
    def get_single_user(cls,data):
        query = "SELECT * FROM users left join Hobbies ON hobbies.user_id = users.id where users.id = %(id)s"
        results = connectToMySQL(db).query_db(query,data)
        pprint.pprint(results, sort_dicts=False)
        user = cls(results[0])
        for hobby in results: 
            hobby_dictionary = {
                'id': hobby['Hobbies.id'],
                'activity' : hobby['activity'],
                'exp_lvl' : hobby['exp_lvl'],
                'created_at' : hobby['created_at'],
                'updated_at' : hobby['updated_at']
            }
            user.hobbies.append(Hobby(hobby_dictionary))
        return user
    

    @classmethod
    def update_user(cls,data,id):
        query = f'''
        UPDATE users
        set name = %(name)s, username = %(username)s, email = %(email)s, password = %(password)s
        WHERE id = {id}
        '''
        return connectToMySQL(db).query_db(query,data)
    
    @classmethod
    def delete_user(cls,id):
        query = f"DELETE  FROM users where id = {id}"
        results = connectToMySQL(db).query_db(query)

    @staticmethod
    def user_validator(user):
        is_valid = True
        if len(user['name']) < 6:
            flash("your name is not long enough!")
            is_valid = False

        if len(user['username']) < 4:
            flash("your name is not long enough!")
            is_valid = False

        if not EMAIL_REGEX.match(user['email']):
            flash("your email is invalid!")
            is_valid = False

        if len(user['password']) < 8:
            if not PASWORD_REGEX.match(user['password']):
                flash("your password is invalid!, must have 1 uppercase, 1 lowercase, 1 digit, 1 specail character")
                is_valid = False

        if not user['password'] == user['cpass']:
            flash("your password do not match!")
            is_valid = False

        return is_valid