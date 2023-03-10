from flask_app.config.mysqlconnection import connectToMySQL
import pprint
from flask import flash

db = "hobby_dobby"

class Hobby:
    def __init__(self,data):
        self.id = data['id']
        self.exp_lvl = data['exp_lvl']
        self.activity = data['activity']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def save(cls,data):
        query = "INSERT INTO hobbies (activity,exp_lvl,user_id) VALUES (%(activity)s, %(exp_lvl)s, %(user_id)s)"
        return connectToMySQL(db).query_db(query,data)


    @staticmethod
    def hobby_validator(hobby):
        is_valid = True

        if len(hobby['activity']) < 2:
            flash("your hobby needs to be atleast two characters long")
            is_valid = False

            if len(hobby['exp_lvl']) < 3:
                flash ("experince level must be atleast 3 character long")
                is_valid = False
        return is_valid

