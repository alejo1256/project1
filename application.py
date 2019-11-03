import os
import csv
import requests

from flask import Flask, session, request, render_template, redirect, url_for, flash
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

app = Flask(__name__)


# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))


# open csv file
def main():
    f = open("books.csv")
    reader = csv.reader(f)
    for isbn, title, author, year in reader:
        db.execute("INSERT INTO books (isbn, title, author, year) VALUES (:isbn, :title, :author, :year)",
            {"isbn": isbn, "title": title, "author": author, "year": year})
        print(f"Added books as {isbn}, {title}, {author}, {year}.")
    db.commit()

#about section

@app.route('/about')
def about():
    return render_template('about.html')

#signup
@app.route("/signup", methods=['GET','POST'])
def signup():
    
    username = request.form.get("username")
    password = request.form.get("password")

    if request.method == "POST":
        db.execute("INSERT INTO users (username, password) VALUES (:username, :password)",
            {"username": username, "password": password})
        db.commit()
        return render_template("success.html")
    
    return render_template("signup.html")


#login
@app.route("/login/", methods=['GET', 'POST'])
def login():
    if request.method == "POST":

        #Get form fields
        username = request.form.get("username")
        password = request.form.get("password")

        account = db.execute("SELECT * FROM users WHERE username = :username AND password = :password", 
        {"username": username , "password": password}).fetchone()

        if account is None:
            message = "Username not found."
            return render_template("error.html", message=message)
        else:
            session['loggedin'] = True
            session['username'] = username

            return redirect(url_for('home'))
            
    return render_template("login.html")

#log out
@app.route("/logout")
def logout():
    session.clear()
    message = "Successfully logged out"
    return render_template("success.html", message=message)



# home page
@app.route("/home")
def home():

    if 'loggedin' in session:
        message = "Welcome Back"
        return render_template('home.html', username=session['username'], message=message)
   


@app.route("/")
def index():
    return render_template('index.html')





if __name__ == '__main__':
    main()
    app.debug = True
    app.run()
