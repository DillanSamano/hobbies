from flask_app import app
from flask import render_template, request, redirect, session
from flask_app.models.user_model import User 
from flask_app.models.hobby_model import Hobby

@app.route('/create_hobby')
def show_create_hobby_page():
    users = User.get_all()
    return render_template("create_hobby.html", users = users)


@app.route("/create_hobby", methods = ['post'])
def create_hobby():
    if not Hobby.hobby_validator(request.form):
        return redirect("/create_hobby")
    Hobby.save(request.form)
    return redirect("/success") 