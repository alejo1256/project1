import os
import csv

from flask import Flask, session, request, render_template
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

#registration
@app.route("/signup", methods=['GET','POST'])
def signup():

    user_id = 0
    username = request.form.get("username")
    password = request.form.get("password")

    if request.method == "POST":
        db.execute("INSERT INTO users (user_id, username, password) VALUES (:user_id + 1, :username, :password)",
            {"user_id": user_id, "username": username, "password": password})
        db.commit()

    # flash('You just signed up! Redirecting back to home page')

    # redirect(url_for('index'))

    return render_template("signup.html")


@app.route("/")
def index():
    return render_template('index.html')





if __name__ == '__main__':
    main()
    app.debug = True
    app.run()
