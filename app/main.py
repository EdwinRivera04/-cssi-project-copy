from bson import ObjectId
import requests
import email
import pymongo
import dns 
from flask import Flask,render_template, request, url_for, redirect, session
from pymongo.server_api import ServerApi
import bcrypt
import os
import random


app=Flask(__name__)
app.secret_key = 'testj g'
connstring = "mongodb+srv://eddy:WVIzKi0UqwTw6Dg5@cluster0.uifhgot.mongodb.net/?retryWrites=true&w=majority"

client = pymongo.MongoClient(connstring, server_api=ServerApi('1'))





db = client.get_database('total_records')
records=db.register
matches = db.matches


user_data = {
    "user": "",
    "liked_count": 0,
    "disliked_count": 0
}

    

@app.route("/", methods=["POST", "GET"])
def login():
    message = 'Please login to your account'
    if "email" in session:
        return redirect(url_for("logged_in"))

    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

       
        email_found = records.find_one({"email": email})
        if email_found:
            email_val = email_found['email']
            passwordcheck = email_found['password']
            
            if bcrypt.checkpw(password.encode('utf-8'), passwordcheck):
                session["email"] = email_val
                return redirect(url_for("logged_in"))
            else:
                if "email" in session:
                    return redirect(url_for("index"))
                message = 'Wrong password'
                return render_template('login.html', message=message)
        else:
            message = 'Email not found'
            return render_template('login.html', message=message)
    return render_template('login.html', message=message)


@app.route("/register", methods=['post', 'get'])
def index():
    message = ''
    if "email" in session:
        return redirect(url_for("logged_in"))
    if request.method == "POST":
        #user = request.form.get("fullname")
        email = request.form.get("email")
        
        password1 = request.form.get("password")
        # password2 = request.form.get("password2")
        
        #user_found = records.find_one({"name": user})
        email_found = records.find_one({"email": email})
        #if user_found:
         #   message = 'There already is a user by that name'
        #    return render_template('register.html', message=message)
        if email_found:
            message = 'This email already exists in database'
            return render_template('register.html', message=message)
        #if password1 != password2:
            # message = 'Passwords should match!'
            # return render_template('register.html', message=message)
        else:
            hashed = bcrypt.hashpw(password1.encode('utf-8'), bcrypt.gensalt())
            user_input = {'email': email, 'password': hashed, 'liked_count': 0, 'disliked_count': 0}
            records.insert_one(user_input)
            
            user_data = records.find_one({"email": email})
            new_email = user_data['email']
   
            return redirect(url_for("logged_in"))
    return render_template('register.html')

@app.route('/logged_in')
def logged_in():
    if "email" in session:
        email = session["email"]
        return render_template('logged_in.html', email=email)
    else:
        return redirect(url_for("login"))

@app.route('/index',methods=['POST','GET'])
def swipe():
    if "email" in session:
        if request.method == 'POST' and request.form.get('like') == 'like':
            data = callAPI() 
            imgsrc = data["download_url"]
            author = data["author"]
            email = session["email"]
            email_user = session['email']
            filter = { "email": email_user }
            newvalues = { "$inc": { "liked_count": 1 } }
            records.update_one(filter, newvalues)

            return render_template('index.html', email=email,imgsrc=imgsrc,author=author)
        elif request.method == 'POST' and request.form.get('dislike') == 'dislike':
            data = callAPI() 
            imgsrc = data["download_url"]
            author = data["author"]
            email = session["email"]
            email_user = session['email']
            filter = { "email": email_user }
            newvalues = { "$inc": { "disliked_count": 1 } }
            records.update_one(filter, newvalues)
            
            return render_template('index.html', email=email,imgsrc=imgsrc,author=author)
        else: 
            data = callAPI() 
            imgsrc = data["download_url"]
            author = data["author"]
            email = session["email"]
            return render_template('index.html', email=email,imgsrc=imgsrc,author=author)
    else:
        return redirect(url_for("login"))


@app.route("/logout", methods=["POST", "GET"])
def logout():
    if "email" in session:
        email = session["email"]
        session.pop("email", None)
        return render_template("logout.html", email=email)
    else:
        return render_template('index.html')


@app.route("/api", methods=["POST","GET"])
def callAPI():
    url = f"https://picsum.photos/id/{random.randint(0,1084)}/info"
    try:
        response = requests.get(url)
        data = response.json()
        return data
    except requests.exceptions.RequestException as e:
        raise SystemExit(e)
        


#end of code to run it
if __name__ == "__main__":
  app.run(debug=True)
