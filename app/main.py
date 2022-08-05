import requests
import email
import pymongo
import dns 
from flask import Flask,render_template, request, url_for, redirect, session
from pymongo.server_api import ServerApi
import bcrypt
import os
import random
import regex as re




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

regex = r'^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'  
  
def checkEmail(email):   
    if(re.search(regex,email)):   
        return True
    return False



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
        elif checkEmail(email):
            hashed = bcrypt.hashpw(password1.encode('utf-8'), bcrypt.gensalt())
            user_input = {'email': email, 'password': hashed, 'liked_count': 0, 'disliked_count': 0}
            records.insert_one(user_input)
            
            user_data = records.find_one({"email": email})
            new_email = user_data['email']
            return redirect(url_for("logged_in"))
        else:
            message = 'Use an actual email.'
            return render_template('register.html', message=message) 
   

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
        data = callAPI()
        imgsrc = data["download_url"]
        author = data["author"]
        email = session["email"]
        if request.method == 'POST':
            if request.form.get('like') == 'like':
                data = callAPI() 
                filter = { "email": email }
                newvalues = { "$inc": { "liked_count": 1 } }
                records.update_one(filter, newvalues)

                return render_template('index.html', email=email,imgsrc=imgsrc,author=author)
            if request.form.get('dislike') == 'dislike':
                data = callAPI() 
                filter = { "email": email }
                newvalues = { "$inc": { "disliked_count": 1 } }
                records.update_one(filter, newvalues)
            
                return render_template('index.html', email=email,imgsrc=imgsrc,author=author)
            if  request.form.get('similar') == 'similar':
                user_data = records.find_one({"email": email})
                num_count = user_data['liked_count']
                similar_users = records.find( {"liked_count":{"$gt": num_count-2, "$lt": num_count+2}},{"email":1,"_id":0})
            # Iterates through users with number greater than theirs and then adds to array
                similar_array = []
                for x in similar_users:
                    for y in x.keys():
                        if email != x[y]: 
                            similar_array.append(x[y])
                imgsrc = data["download_url"]
                author = data["author"]
                
                return render_template('index.html', email=email,imgsrc=imgsrc,author=author,similar_array=similar_array)


        else: 
            data = callAPI() 
            return render_template('index.html', email=email,imgsrc=imgsrc,author=author)
    else:
        return redirect(url_for("login"))


@app.route("/logout", methods=["POST", "GET"])
def logout():
    if "email" in session:
        email = session["email"]
        session.pop("email", None)
        return redirect(url_for("login"))
    else:
        return redirect(url_for("login"))


@app.route("/api", methods=["POST","GET"])
def callAPI():
    url = f"https://picsum.photos/id/{random.randint(0,1084)}/info"
    try:
        response = requests.get(url,timeout=25)
        data = response.json()
        return data
    except requests.exceptions.RequestException as e:
        raise SystemExit(e)
        


#end of code to run it
if __name__ == "__main__":
  app.run(debug=True)
