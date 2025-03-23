from flask import Blueprint,render_template
from flask import request
from flask import Response
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from redis_client import get_token_by_email, redis_connection, save_token
import json
from client_user import *

gateway = Blueprint('routes', __name__)

def general_response(json_data: any):

    return Response(json.dumps(json_data, ensure_ascii=False), content_type='application/json; charset=utf-8')

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
    
@gateway.route('/student', methods=['GET'])
def stutent():

    data = get_student()

    return general_response(data)

@gateway.route('/state', methods=['GET'])
def state():

    data = get_state()

    return general_response(data)

@gateway.route('/gender', methods=['GET'])
def gender():

    data = get_gender()

    return general_response(data)

"""@gateway.route('/payment', method=['GET'])
def payment():

    return True

@gateway.route('/plan', method=['GET'])
def plan():

    return True"""
    




    