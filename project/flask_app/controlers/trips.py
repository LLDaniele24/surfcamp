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
stripe.api_key = 'sk_test_51NVKGNDLPPkt7yRXuE7pbLoefAejYL3IR6cGguBZQmgY4wSgWdISbF7TEiTU2Wxop8m4yHt6UZNb4eZprIo3cy0n00AFKz5dvk'
YOUR_DOMAIN='http://127.0.0.1:4242'


@app.route('/create_trip')
def create_trip():
    if 'user_id' not in session:
        return redirect('/')
    data = {
        'id':session['user_id']
    }
    user=User.get_by_id(data)
    return render_template('create_trip.html',user=user)



#ad the trip to the db
@app.route ('/reserve_trip' ,methods=['POST'])
def reserve_trip():
    if 'user_id' not in session:
        return redirect('/')
    data = {
        'day': request.form['day'],
        'time':request.form['time'],
        'pickup_location':request.form['pickup_location'],
        'destination':request.form['destination'],
        'level':request.form['level'],
        'board':request.form['board'],
        'user_id':session['user_id']

    }
    Trip.create_trip(data)
    return redirect('/account')

#dispaly one trip
@app.route('/show_trip/<int:trip_id>')
def show_trip(trip_id):
    if 'user_id' not in session:
        return redirect('/')
    data = {
        'id':session['user_id']
    }
    trip_data={
        'id': trip_id
    }

    user=User.get_by_id(data)
    reservation=Trip.together(trip_data)
    #liked_owner=Trip.like_owner(like_data)
    return render_template('display_trip.html',user=user,reservation=reservation)





@app.route('/check_out')
def payment():
    if 'user_id' not in session:
        return redirect('/')
    data = {
        'id':session['user_id']
    }
    user=User.get_by_id(data)
    return render_template('/checkout.html',user=user)






##stripe check out
@app.route('/payment',methods=['POST'])
def check_out():
    data = {
        'id':session['user_id']
    }
    try:
        checkout_session = stripe.checkout.Session.create(
            line_items=[
                {
                    # Provide the exact Price ID (for example, pr_1234) of the product you want to sell
                    'price': 'price_1NVKH6DLPPkt7yRXXvOBhPHj',
                    'quantity': 1,
                },
            ],
            mode='payment',
            success_url=YOUR_DOMAIN+'/thank_you.html'
           
        )
    except Exception as e:
        return str(e)
    card_data = {
        'name': request.form['name'],
        'card_number':request.form['card_number'],
        'ex_month':request.form['ex_month'],
        'ex_year':request.form['ex_year'],
        'cvc':request.form['cvc'],
        'user_id':session['user_id']

    }
    
    Trip.save_payment(card_data)
    
    if not Trip.validate_card(request.form):
        return redirect('/check_out')
    
    user=User.get_by_id(data)
    return render_template('thank_you.html',user=user,code=303)




#like and dislike
@app.route('/like/<int:trip_id>')
def like(trip_id):
    data={
        'trip_id':trip_id,
        'user_id':session['user_id']
    }
    Trip.like(data)
    return redirect('/account')



@app.route('/dislike/<int:trip_id>')
def dislike(trip_id):
    data={
        'trip_id':trip_id,
        'user_id':session['user_id']
    }
    Trip.dislike_trip(data)
    return redirect('/account')





@app.route('/delete/<int:trip_id>')
def delete_trip(trip_id):
    if 'user_id' not in session:
        return redirect('/')
    data={
        'id': trip_id
    }
    
    Trip.delete(data)

    return redirect('/account')