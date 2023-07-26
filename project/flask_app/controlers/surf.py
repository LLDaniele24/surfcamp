from flask import Flask,render_template,request,session,redirect,url_for
from flask_app import app
from flask_app.models.trip_model import Trip
from flask_app.models.user import User
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)
from flask import flash
import os
import requests
from pprint import pprint
#stripe is for payments
import stripe
import json
import bs4 
from bs4 import BeautifulSoup


stripe.api_key = 'sk_test_51NVKGNDLPPkt7yRXuE7pbLoefAejYL3IR6cGguBZQmgY4wSgWdISbF7TEiTU2Wxop8m4yHt6UZNb4eZprIo3cy0n00AFKz5dvk'
YOUR_DOMAIN='http://127.0.0.1:4242'
surf_key='fd1ef0232cmsh1a2602df8b9c988p1f3768jsndf458877c8bd'


@app.route('/surf_report')
def surf():
    return render_template('surf.html')






@app.route('/surf',methods=['POST'])
def api_surf():

    #querystring = {"name":"avellanas"}
    surfbreak=request.form['surfbreak']
    headers = {
        "X-RapidAPI-Key": "d12e1b958bmsh916f5df4da154efp14cbb5jsnb07966177f3b",
        "X-RapidAPI-Host": "simple-surf-forecast-api1.p.rapidapi.com"
    }

    response = requests.get( url = f"https://simple-surf-forecast-api1.p.rapidapi.com/api/surfbreaks={surfbreak}", headers=headers)#,params=querystring)
    surf_data= response.json()
    #session['name']=surf_data['name']
    #session['feels_like']=weather_data['main']['feels_like']
    # to take only one item from the dictionary use ['main']['temp']
    #session['wind']=surf_data['wind']['speed']
    #session['sunrise']=surf_data['sys']['sunrise']
    #session['sunset']=weather_data['sys']['sunset']

    pprint(response.json()) 
    return redirect ('/surf_report')  


@app.route('/check_accomodations')
def accomodations():
    
    return("https://www.airbnb.com/s/Tamarindo--Guanacaste-Province--Costa-Rica/homes?adults=2&checkin=2023-07-25&checkout=2023-07-31")