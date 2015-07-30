"""Movie Ratings."""

from jinja2 import StrictUndefined

from flask import Flask, render_template, redirect, request, flash, session
from flask_debugtoolbar import DebugToolbarExtension

from model import User, Rating, Movie, connect_to_db, db


app = Flask(__name__)


# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# Normally, if you use an undefined variable in Jinja2, it fails silently.
# This is horrible. Fix this so that, instead, it raises an error.
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """Homepage."""

    return render_template("homepage.html")

@app.route('/users')
def user_list():
    """Show list of all zee uzerz in zee database"""

    users = User.query.all()
    return render_template("user_list.html", users=users)


@app.route('/login', methods=["GET", "POST"])
def login():
    """A form to login to the movie site with your username and password"""

    if request.method == "GET":
        return render_template("login_form.html")

    else:
        email = request.form.get("email")


        this_user = User.query.filter(User.email == email).first()



        print this_user
        print "\n\n\n\n\n"


        if this_user:

            session["email"] = email

            flash("Thanks %s. You are now logged in!" % (session['email']))

            user_id = this_user.user_id
    
            return redirect('/users/' + str(user_id)) #redirect takes a string as an input! 
        else: 
            new_user = User(email=email)
            db.session.add(new_user)
            db.session.commit()

            session["email"] = email

            flash("Thanks %s. Welcome to Movie Ratings! You're logged in. Have fun." % (session['email']))

            user_id = new_user.user_id

            return redirect('/users/' + str(user_id)) #redirect takes a string as an input! 


@app.route('/logout', methods=['GET', 'POST'])  
def logout():
    """ Logs the current user out. Clears the session."""

    del session["email"]
    del session["password"]

    flash("Logged Out")

    return redirect('/')     


@app.route('/users/<string:user_id>') # need syntax for variable username 
def user_details(user_id):
    """ Displays information about selected user. """

    user_object = User.query.filter(User.user_id == user_id).one()

    user_id = user_object.user_id
    email = user_object.email
    age = user_object.age
    zipcode = user_object.zipcode
  
    return render_template("user_details.html", user_id=user_id, email=email, age=age, zipcode=zipcode)

if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension
    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)
    print "\n\n\nYO\n\n\n"
    app.run()