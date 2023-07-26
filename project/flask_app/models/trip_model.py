from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import user
import re
from pprint import pprint
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

db="project"
class Trip:
    def __init__( self , data ):
        self.id = data['id']
        self.day =data['day']
        self.time= data['time']
        self.pickup_location= data['pickup_location']
        self.destination=data['destination']
        self.level = data['level']
        self.board=data['board']
        self.created_at=data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']
        self.owner=None
        self.all_likes=[]
        self.owner_like=None



    @classmethod
    def create_trip(cls, data):
        query = ''' INSERT INTO trips ( day,time,pickup_location,destination,level,board,user_id)
        VALUES ( %(day)s ,%(time)s ,%(pickup_location)s ,%(destination)s, %(level)s ,%(board)s,%(user_id)s);'''
        return connectToMySQL('project').query_db( query, data )

        
    #display all trips
    @classmethod
    def get_all(cls,data):
        query ="SELECT * from trips"
        results= connectToMySQL('project').query_db(query,data)
        trips=[]
        for trip in results:
            trips.append(cls(trip))

        return trips

    @classmethod
    def one_trip(cls,data):
        query="SELECT * FROM trips WHERE id =%(id)s"
        results= connectToMySQL('project').query_db(query,data)
        return cls(results[0])
        
    

    
    #display surf trip 
    @classmethod 
    def together(cls,data):
        query = "SELECT * from trips JOIN users ON users.id=trips.user_id WHERE trips.id=%(id)s;"
        results= connectToMySQL('project').query_db(query,data)
        trips = cls(results[0])
        user_data={
            'id': results[0]['users.id'],
            'first_name':results[0]['first_name'],
            'last_name':results[0]['last_name'],
            'email':results[0]['email'],
            'password':results[0]['password'],
            'created_at':results[0]['created_at'],
            'updated_at':results[0]['updated_at']

        }
        trips.owner = user.User(user_data)
        return trips


    
    @classmethod
    def like(cls,data):
        query="INSERT INTO likes(user_id,trip_id) VALUES (%(user_id)s,%(trip_id)s)"
        return connectToMySQL('project').query_db(query,data)
    
    @classmethod
    def dislike_trip(cls,data):
        query="DELETE FROM likes WHERE trip_id=%(trip_id)s AND user_id=%(user_id)s"
        return connectToMySQL('project').query_db(query,data)
    
    @classmethod
    def all_that_liked(cls):
        query='''
            SELECT * FROM trips
            JOIN users ON users.id = trips.user_id
            LEFT JOIN likes ON trips.id = likes.trip_id
            LEFT JOIN users AS users2 ON users2.id = likes.user_id
            '''
        results=connectToMySQL('project').query_db(query)
        pprint(results)
        likes=[]
        for x in results:
            new_like=True
            user_trip_that_got_liked_data ={
                'id': x['users2.id'],
                'first_name':x['users2.first_name'],
                'last_name':x['users2.last_name'],
                'email':x['users2.email'],
                'password':x['users2.password'],
                'created_at':x['users2.created_at'],
                'updated_at':x['users2.updated_at']
            }
            if len(likes)> 0 and likes[len(likes)-1].id == x['id']:
                likes[len(likes)-1].all_likes.append(user.User(user_trip_that_got_liked_data))
                new_like=False
            if new_like:
                like=cls(x)
                user_data={
                    'id': x['users.id'],
                    'first_name':x['first_name'],
                    'last_name':x['last_name'],
                    'email':x['email'],
                    'password':x['password'],
                    'created_at':x['created_at'],
                    'updated_at':x['updated_at']
                }
                user2=user.User(user_data)
                like.user=user2
                if x['users2.id'] is not None:
                    like.all_likes.append(user.User(user_trip_that_got_liked_data))
                likes.append(like)
        pprint(likes)
        return likes


    #@classmethod
    #def like_owner(cls,data):
        #query ='''
        #SELECT * from likes JOIN users on users.id=likes.user_id WHERE likes.id=%(id)s;
        #'''
        #results=connectToMySQL('project').query_db(query,data)
        #liked=cls(results[0])
        #user_that_liked={
            #'id': results[0]['users.id'],
            #'first_name':results[0]['first_name'],
            #'last_name':results[0]['last_name'],
            #'email':results[0]['email'],
            #'password':results[0]['password'],
            #'created_at':results[0]['created_at'],
            #'#updated_at':results[0]['updated_at']
        #}
        #liked.owner_like=user.User(user_that_liked)
        #return liked

    
    
    @classmethod
    def delete(cls,data):
        query=" DELETE FROM trips WHERE id=%(id)s;"
        results=connectToMySQL('project').query_db(query,data)
        return results



    @staticmethod
    def validate_card(data):
        is_valid =True
        if len(data['name']) <= 1:
            flash("Name must be more than one character !!!")
            is_valid=False
        if len(data['card_number'])<= 1:
            flash("card number must be more than one charachter!!!")
            is_valid=False
        if len(data['ex_month']) == 0:
            flash('invalid month!!')
            is_valid=False
        if len(data['ex_year'])==0:
            flash('invalid year!')
            is_valid=False
        if len(data['cvc'])==0:
            flash("invalid!!")
            is_valid=False


        return is_valid
    
    @classmethod
    def save_payment(cls,data):
        query='''INSERT INTO payments(name,card_number,ex_month,ex_year,cvc,user_id) 
        VALUES (%(name)s,%(card_number)s,%(ex_month)s,%(ex_year)s,%(cvc)s,%(user_id)s)
        '''
        return connectToMySQL('project').query_db(query,data)