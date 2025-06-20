from flask import Blueprint,request,send_file
from flask_jwt_extended import create_access_token
import requests
from redis_client import get_token_by_email, save_token
from client_user import *
from client_financial import *
from utils import *

gateway = Blueprint('routes', __name__)

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

        print(json)

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
        nivel_id = int(json.get('nivel'))
        goal_id = int(json.get('goal'))

        student_id = create_student(name,gender_id,birthday,email,phone,state_id,city,neighborhood,address,number,cep,payment_id,nivel_id,goal_id)  

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
        nivel_id = int(json.get('nivel'))
        goal_id = int(json.get('goal'))


        student_status = update_student(id,name,gender_id,birthday,email,phone,state_id,city,neighborhood,address,number,cep,payment_id,nivel_id,goal_id)

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

    print(name)

    data = get_student_by_name(name)

    return data

@gateway.route('/nivel', methods=['GET'])
def nivel():

    data = get_nivel()

    nivel_list = [
        {
            "id": item['id'],
            "name": format_general_name(item['name']),
        }
        for item in data
    ]

    return general_response(nivel_list)

@gateway.route('/goal', methods=['GET'])
def goal():

    data = get_goal()

    goal_list = [
    {
        "id": item['id'],
        "name": format_general_name(item['name']),
    }
    
    for item in data
    ]

    return general_response(goal_list)

@gateway.route('/ai', methods=['POST'])
def ai():

    req_data = request.get_json()

    plan = req_data.get('plan')
    nivel = req_data.get('nivel')
    goal = req_data.get('goal')
    student = req_data.get('student')

    response_from_ai_server = requests.post(
        'http://ai_server:5002/fitai',
        json={'plan': plan, 'nivel': nivel}
    )

    ai_data = response_from_ai_server.json()

    unformat_plan = unformat_general_name(plan)

    unformat_nivel = unformat_general_name(nivel)

    unformat_goal = unformat_general_name(goal)

    pdf_stream = generate_pdf_to_download(ai_data, student, unformat_plan, unformat_nivel, unformat_goal)

    return send_file(
        pdf_stream,
        mimetype='application/pdf', 
        as_attachment=True,
        download_name=f'plano_de_treino_{student}.pdf' 
    )



    