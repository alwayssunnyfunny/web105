from flask import Flask, render_template, request, session, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = 'your_secret_key' 

# Configure SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:admin@localhost:5432/flas_database'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Define your models using db.Model

class Semester(db.Model):
    semester_id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(50), nullable=False)
    
class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(30), nullable=False)
    registration_date = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())
    semester_id = db.Column(db.Integer, db.ForeignKey('semester.semester_id'))


class UsersSem(db.Model):
    __tablename__ = 'users_sem'
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), primary_key=True)
    semester_id = db.Column(db.Integer, db.ForeignKey('semester.semester_id'), primary_key=True)

class Subject(db.Model):
    subject_id = db.Column(db.Integer, primary_key=True)
    subject_name = db.Column(db.String(80), unique=True, nullable=False)
    sem_id = db.Column(db.Integer, db.ForeignKey('semester.semester_id'), nullable=False)

class UserSubjects(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    subject_id = db.Column(db.Integer, db.ForeignKey('subject.subject_id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)

class SubjectDescription(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    avg_marks = db.Column(db.Integer)
    description = db.Column(db.String(100))
    resources = db.Column(db.String(200))
    subject_id = db.Column(db.Integer, db.ForeignKey('subject.subject_id'))

# Create tables
with app.app_context():
    db.create_all()

# Define routes
@app.route("/home")
def home():
    return render_template("home.html")

@app.route("/hello")
def hello():
    return render_template("hello.html")

def is_valid_email(email):
    # Ensure email ends with '@email.com'
    return email.lower().endswith('@email.com')

@app.route("/loginhello", methods=["GET", "POST"])
def loginhello():
    email=None
    if request.method == "POST":
        user = request.form["username-email"]
        if is_valid_email(user):
            session["user"] = user   
            
            return redirect(url_for("user"))
            
        else:
            flash("Invalid email format. Please use an email ending with '@email.com'.")

        return redirect(url_for("user")) 
        
    elif "user" in session:
        return redirect(url_for("user"))  
    
    return render_template("loginhello.html")

@app.route("/sign")
def sign():
    return render_template("sign.html")

@app.route("/user")
def user():
    if "user" in session:
        user = session["user"]
        return render_template("subject.html")
    else:
        return redirect(url_for("loginhello"))  

if __name__ == '__main__':
    app.run(debug=True)
