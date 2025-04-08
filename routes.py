from flask import Blueprint,render_template
from flask import request
from flask import Response
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from redis_client import get_token_by_email, redis_connection, save_token
import json
from client_user import *
from client_financial import *
from flask import jsonify

gateway = Blueprint('routes', __name__)

def update_student_id_and_financial_id(student_id, financial_id):

    student_status = update_financial_id_by_student_id(student_id, financial_id)

    financial_status = update_student_id_by_financial_id(student_id, financial_id)

    if financial_status["success"] and student_status["success"]:

        data = { "status" : True }

        return data 
        
    else:

        data = { "status" : False }

        return data

def delete_student_id_and_payment_id(student_id, payment_id):

    student_status = delete_student_by_id(student_id)

    payment_status = delete_payment_by_id(payment_id)

    if payment_status["success"] and student_status["success"]:

        data = { "status" : True }

        return data 
        
    else:

        data = { "status" : False }

        return data

def general_response(json_data):
    
    return jsonify(json_data)  

def check_token(email, token):

    redis_token = get_token_by_email(email)

    return token == redis_token

@gateway.route('/authenticate', methods=['POST'])
def authenticate():

    data = request.get_json()

    email = data.get('email')
    password = data.get('password')
    token = data.get('auth_token')

    success = authenticate_user(email, password)

    if success:

        if token == '0':

            token = create_access_token(identity=email)

            expiration_time = 3600

            save_token(email,token,expiration_time)
        
            return general_response(token)
        
        else:

            redis_token = get_token_by_email(email)

            if redis_token == token:

                return general_response(token)
            else:
                return general_response(redis_token)          
        
    else:

        return general_response("User Not Found")
    
@gateway.route('/student', methods=['GET', 'POST', 'PUT', 'DELETE'])
def stutent():

    if request.method == 'GET':

        data = get_student()

    elif request.method == 'POST':

        json = request.get_json()

        id = int(json.get('id'))
        name = json.get('name')
        email = json.get('email')
        gender_id = int(json.get('gender'))
        birthday = json.get('birthdate')
        phone = json.get('phone')
        state_id = int(json.get('state'))
        city = json.get('city')
        neighborhood = json.get('neighborhood')
        address = json.get('address')
        number = json.get('number')
        plan = int(json.get('plan'))
        cep = json.get('cep')
        payment_id = int(json.get('payment'))
        method_id = int(json.get('method'))

        student_id = create_student(name,gender_id,birthday,email,phone,state_id,city,neighborhood,address,number,cep,payment_id)  

        financial_id = create_payment(id,plan,method_id)

        data = {"status" : update_student_id_and_financial_id(student_id["id"], financial_id["id"])}

        return data


    elif request.method == 'PUT':

        json = request.get_json()

        id = int(json.get('id'))
        name = json.get('name')
        email = json.get('email')
        gender_id = int(json.get('gender'))
        birthday = json.get('birthdate')
        phone = json.get('phone')
        state_id = int(json.get('state'))
        city = json.get('city')
        neighborhood = json.get('neighborhood')
        address = json.get('address')
        number = json.get('number')
        plan = int(json.get('plan'))
        cep = json.get('cep')
        payment_id = int(json.get('payment'))
        method_id = int(json.get('method'))

        student_status = update_student(id,name,gender_id,birthday,email,phone,state_id,city,neighborhood,address,number,cep,payment_id)

        payment_status = update_payment(payment_id,id,plan,method_id)

        if payment_status["status"] and student_status["status"]:

            data = { "status" : True }

            return data 
        
        else:

            data = { "status" : False }

            return data 
        
    
    elif request.method == 'DELETE':
    
        json = request.get_json()

        student_id = json.get('student_id')
        payment_id = json.get('payment_id')
    
        data = delete_student_id_and_payment_id(student_id,payment_id)

    return data

@gateway.route('/state', methods=['GET'])
def state():

    data = get_state()

    return general_response(data)

@gateway.route('/gender', methods=['GET'])
def gender():

    data = get_gender()

    return general_response(data)

@gateway.route('/plan', methods=['GET'])
def plan():

    data = get_plan()

    return general_response(data)

@gateway.route('/method', methods=['GET'])
def method():

    data = get_method()

    return general_response(data)

@gateway.route('/search', methods=['POST'])
def search():

    json = request.get_json()

    name = json.get('name')

    data = get_student_by_name(name)

    return data


    




    