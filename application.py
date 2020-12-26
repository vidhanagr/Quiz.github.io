from flask import Flask, render_template, request, session, redirect
import sqlite3

app = Flask(__name__)
app.secret_key = "xjkhadgUsdagd14rf"

def authenticateUser(username, password):

    conn = sqlite3.connect('userdata.db')
    cur = conn.cursor()

    cur.execute("SELECT password FROM user WHERE username=?", (username,))
    result = cur.fetchone()

    cur.close()
    conn.close()

    print('Password obtained from DB is', result)

    return False if result is None or result[0] != password else True

def addToDatabase(fname, email, username, password):

    conn = sqlite3.connect('userdata.db')
    cur = conn.cursor()

    cur.execute("INSERT INTO user(fname, email, username, password) VALUES(?, ?, ?, ?)",
     (fname, email, username, password))

    conn.commit()

    cur.close()
    conn.close()

    print('User added to DB', (fname, email, username, password))

@app.route('/', methods=["GET", "POST"])
def homepage():
    ''' Homepage of the website '''

    return render_template("index.html")

@app.route('/login', methods=["GET", "POST"])
def login():
    ''' Login page for users '''

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        if authenticateUser(username, password):
            session["user"] = username
            return redirect("/movies")
        else:
            return render_template("login.html")

    elif "user" in session:
        return redirect("/movies")

    else:
        return render_template("login.html")

@app.route('/movies', methods=["GET", "POST"])
def landingPage():
    """ Movie section """

    if "user" in session:
        if request.method == "POST":
            movietype = request.form["movietype"]
            return render_template("movies.html", movietype=movietype)
        else:
            return render_template("movies.html")
    else:
        return redirect("/login")

@app.route('/logout', methods=["GET", "POST"])
def logout():
    """ User logout """

    session.pop("user", None)
    return redirect("/")

@app.route('/register', methods=["GET", "POST"])
def createAccount():
    """ Register an account """

    if request.method == "GET":
        return render_template("register.html")

    else:

        fname = request.form["fname"]
        email = request.form["email"]
        username = request.form["username"]
        password = request.form["password"]

        addToDatabase(fname, email, username, password)

        return redirect("/login")


if __name__ == "__main__":
    app.run(debug=True,port=80)
