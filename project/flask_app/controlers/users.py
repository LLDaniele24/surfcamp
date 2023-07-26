from flask import Flask,render_template,request,session,redirect
from flask_app import app
from flask_app.models.trip_model import Trip
from flask_app.models.user import User
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)
from flask import flash
import os
import requests
from pprint import pprint


@app.route('/')
def index():

    
    return render_template('register.html')




@app.route('/register',methods=['POST'])
def register():
    if not User.validate_user(request.form):
        return redirect('/')
    #pw_hash is a variable
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    print(pw_hash)
    data = {
        "first_name": request.form["first_name"],
        "last_name" : request.form["last_name"],
        "email":request.form["email"],
        "password":pw_hash
    
    }


    user_id=User.save(data)
    session['user_id'] = user_id
    print(user_id)
    return redirect('/dash')


@app.route('/dash')
def dash():
    if 'user_id' not in session:
        return redirect('/')
    data = {
        'id':session['user_id']
    }
    user=User.get_by_id(data)
    

    return render_template('dash.html',user=user)


@app.route('/login')
def dashboard():


    return render_template('login.html')

@app.route('/login_user',methods=["POST"])
def login_user():
        
    user_in_db= User.get_by_email(request.form)
    

    if not user_in_db:
        flash('Invalid email/password')
        return redirect('/')
    
    if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
        flash('Ivalid email/password !!!!')
        return redirect('/')
    session['user_id'] = user_in_db.id
    

    return redirect ('/dash')


@app.route('/account')
def account():
    data = {
        'id':session['user_id']
    }
    user=User.get_by_id(data)
    all_trips= Trip.all_that_liked()
    return render_template('account.html',user=user,all_trips=all_trips)




@app.route('/log_out')
def logout():
    session.clear()
    return render_template('register.html')



@app.route('/show_weather',methods=["POST"])
def show_wether():

    print(request.form['zipcode'])
    #save the info from the Form in html into a variable zip
    zip=request.form['zipcode']
    #use a f string to place a variable {zip} inside so we can use any zipcode then appid = my api key from the website
    call = requests.get(f'https://api.openweathermap.org/data/2.5/weather?zip={zip}&appid=51919b5d9379e09fba871a5b3203a8b0')
    pprint(call.json())
    weather_data= call.json()
    session['city']=weather_data['name']
    session['feels_like']=weather_data['main']['feels_like']
    # to take only one item from the dictionary use ['main']['temp']
    session['wind']=weather_data['wind']['speed']
    session['sunrise']=weather_data['sys']['sunrise']
    session['sunset']=weather_data['sys']['sunset']
    pprint(weather_data['name'])
 
    
    
    #response=requests.get(url, headers={'X-Api-Key': '51919b5d9379e09fba871a5b3203a8b0'})
    #pprint.pprint(response.json())
    #session['weather']= response.json()
    #print(os.environ.get('KEY'))
    return  redirect('/dash')