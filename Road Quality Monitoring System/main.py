from flask import Flask,render_template,request,session,redirect,url_for,flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import login_user,logout_user,login_manager,LoginManager
from flask_login import login_required,current_user
import json

# MY db connection
local_server= True
app = Flask(__name__)
app.secret_key='kusumachandashwini'


# this is for getting unique user access
login_manager=LoginManager(app)
login_manager.login_view='login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))



# app.config['SQLALCHEMY_DATABASE_URL']='mysql://username:password@localhost/databas_table_name'
app.config['SQLALCHEMY_DATABASE_URI']='mysql://root:@localhost/accelerometer'
db=SQLAlchemy(app)

# here we will create db models that is tables


class Trig(db.Model):
    tid=db.Column(db.Integer,primary_key=True)
    XAxis=db.Column(db.String(100))
    action=db.Column(db.String(100))
    timestamp=db.Column(db.String(100))


class User(UserMixin,db.Model):
    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(50))
    email=db.Column(db.String(50),unique=True)
    password=db.Column(db.String(1000))





class AccelerometerData(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    XAxis=db.Column(db.String(50))
    YAxis=db.Column(db.String(50))
    ZAxis=db.Column(db.String(50))
    Latitude=db.Column(db.String(50))
    Longitude=db.Column(db.String(50))
    

@app.route('/')
def index(): 
    return render_template('index.html')

@app.route('/accelerometerdetails')
def accelerometerdetails():
    query=db.engine.execute(f"SELECT * FROM `accelerometerData`")
    return render_template('accelerometerdetails.html',query=query)

@app.route('/triggers')
def triggers():
    query=db.engine.execute(f"SELECT * FROM `trig`") 
    return render_template('triggers.html',query=query)


@app.route("/delete/<string:id>",methods=['POST','GET'])
@login_required
def delete(id):
    db.engine.execute(f"DELETE FROM ` 	accelerometerdata` WHERE `student`.`id`={id}")
    flash("Slot Deleted Successful","danger")
    return redirect('/accelerometerdetails')


@app.route('/signup',methods=['POST','GET'])
def signup():
    if request.method == "POST":
        username=request.form.get('username')
        email=request.form.get('email')
        password=request.form.get('password')
        user=User.query.filter_by(email=email).first()
        if user:
            flash("Email Already Exist","warning")
            return render_template('/signup.html')
        encpassword=generate_password_hash(password)

        new_user=db.engine.execute(f"INSERT INTO `user` (`username`,`email`,`password`) VALUES ('{username}','{email}','{encpassword}')")

        # this is method 2 to save data in db
        # newuser=User(username=username,email=email,password=encpassword)
        # db.session.add(newuser)
        # db.session.commit()
        flash("Signup Succes Please Login","success")
        return render_template('login.html')

          

    return render_template('signup.html')

@app.route('/login',methods=['POST','GET'])
def login():
    if request.method == "POST":
        email=request.form.get('email')
        password=request.form.get('password')
        user=User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password,password):
            login_user(user)
            flash("Login Success","primary")
            return redirect(url_for('index'))
        else:
            flash("invalid credentials","danger")
            return render_template('login.html')    

    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Logout SuccessFul","warning")
    return redirect(url_for('login'))



@app.route('/addaccelerometer',methods=['POST','GET'])
@login_required
def addaccelerometer():
    dept=db.engine.execute("SELECT * FROM `accelerometerdata`")
    if request.method=="POST":
        XAxis=request.form.get('XAxis')
        YAxis=request.form.get('YAxis')
        ZAxis=request.form.get('ZAxis')
        Latitude=request.form.get('Latitude')
        Longitude=request.form.get('Longitude')
        query=db.engine.execute(f"INSERT INTO `accelerometerdata` (`XAxis`,`YAxis`,`ZAxis`,`Latitude`,`Longitude`) VALUES ('{XAxis}','{YAxis}','{ZAxis}','{Latitude}','{Longitude}')")
    

    


    return render_template('accelerometer.html',dept=dept)


app.run(debug=True)    