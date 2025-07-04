import grpc
import service_pb2
import service_pb2_grpc
from flask import jsonify
from client_financial import *
from utils import *

channel = grpc.insecure_channel("user_grpc:50051")

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

def authenticate_user(email, password):
    
    stub = service_pb2_grpc.AuthServiceStub(channel)
    
    request = service_pb2.AuthenticateUserRequest(email=email, password=password)
    
    response = stub.AuthenticateUser(request)  
    
    if response.success:
        return True
    else:
        return False

def get_student():
    try:
        stub = service_pb2_grpc.StudentServiceStub(channel)

        request = service_pb2.StudentDataRequest()

        response = stub.GetStudentData(request)

        students_list = []

        for student in response.student:
        
            student_data = {
                "id": student.id,
                "name": student.name,
                "gender": get_gender_by_id(student.gender_id),
                "birthday": student.birthday,
                "email": student.email,
                "phone": student.phone,
                "state": get_state_by_id(student.state_id),
                "city": student.city,
                "neighborhood": student.neighborhood,
                "address": student.address,
                "number": student.number,
                "cep": student.cep,
                "payment": get_payment_info(student.payment_id),
                "nivel": get_nivel_by_id(student.nivel_id),
                "goal": get_goal_by_id(student.goal_id)
            }
            students_list.append(student_data)

        return jsonify(students_list)


    except grpc.RpcError as e:
        return jsonify({"error": f"Erro ao buscar estudantes: {e}"})

def get_state():

    stub = service_pb2_grpc.StateServiceStub(channel)

    request = service_pb2.StatesDataRequest()

    response = stub.GetStateData(request)

    states_list = [
        {
            "id": state.id,
            "name": state.name,
            "abbreviation": state.abbreviation,
        }
        for state in response.state  
    ]

    return states_list

def get_gender():

    stub = service_pb2_grpc.GenderServiceStub(channel)

    request = service_pb2.GendersDataRequest()

    response = stub.GetGenderData(request)

    gender_list = [
        {
            "id" : gender.id,
            "name": gender.name,
        }
        for gender in response.gender
    ]

    return gender_list

def get_nivel():

    stub = service_pb2_grpc.NivelServiceStub(channel)

    request = service_pb2.NivelDataRequest()

    response = stub.GetNivelData(request)

    nivel_list = [
        {
            "id" : nivel.id,
            "name": nivel.name,
        }
        for nivel in response.nivel
    ]

    return nivel_list

def get_goal():
    
    stub = service_pb2_grpc.GoalServiceStub(channel)

    request = service_pb2.GoalDataRequest()

    response = stub.GetGoalsData(request)

    goal_list = [
        {
            "id": goal.id,
            "name": goal.name,
        }
        for goal in response.goal
    ]

    return goal_list

def get_state_by_id(state_id):

    stub = service_pb2_grpc.StateServiceStub(channel)

    request = service_pb2.StateDataRequestById(state_id=int(state_id))

    response = stub.GetStateDataById(request)

    state_dict = {
        "id" : response.id,
        "name" : response.name,
        "abbreviation" : response.abbreviation,
    }

    return state_dict

def get_gender_by_id(gender_id):

    stub = service_pb2_grpc.GenderServiceStub(channel)

    request = service_pb2.GendersDataRequestById(gender_id=int(gender_id))

    response = stub.GetGenderDataById(request)

    gender_dict = {
        "id" : response.id,
        "name" : response.name,
    }

    return gender_dict

def get_nivel_by_id(nivel_id):

    stub = service_pb2_grpc.NivelServiceStub(channel)

    request = service_pb2.NivelDataRequestById(nivel_id=int(nivel_id))

    response = stub.GetNivelDataById(request)

    nivel_dict = {
        "id" : response.id,
        "name" : format_general_name(response.name),
    }

    return nivel_dict

def get_goal_by_id(goal_id):

    stub = service_pb2_grpc.GoalServiceStub(channel)

    request = service_pb2.GoalDataRequestById(goal_id=int(goal_id))

    response = stub.GetGoalDataById(request)

    goal_dict = {
        "id" : response.id,
        "name" : response.name,
    }

    return goal_dict

def update_student(id,name,gender_id,birthday,email,phone,state_id,city,neighborhood,address,number,cep,payment_id,nivel_id,goal_id):

    stub = service_pb2_grpc.StudentServiceStub(channel)

    request = service_pb2.StudentUpdateRequest(
        id= id,
        name = name,
        gender_id = gender_id,
        birthday = birthday,  
        email = email,  
        phone = phone,
        state_id = state_id, 
        city = city,  
        neighborhood = neighborhood,
        address = address,  
        number = number,  
        cep = cep,
        payment_id = payment_id,
        nivel_id = nivel_id,
        goal_id = goal_id
    )

    response = stub.UpdateStudentData(request)

    response_dict = {
        "status" : response.success
    }

    return response_dict

def create_student(name,gender_id,birthday,email,phone,state_id,city,neighborhood,address,number,cep,payment_id,nivel_id,goal_id):

    stub = service_pb2_grpc.StudentServiceStub(channel)
    
    request = service_pb2.StudentCreateRequest(
        name = name,
        gender_id = gender_id,
        birthday = birthday,
        email = email,
        phone = phone,
        state_id = state_id,
        city = city,
        neighborhood = neighborhood,
        address = address,
        number = number,
        cep = cep,
        payment_id = payment_id,
        nivel_id = nivel_id,
        goal_id = goal_id
    )

    response = stub.CreateStudentData(request)

    response_dict = {
        "id" : response.id
    }

    return response_dict

def update_financial_id_by_student_id(student_id, financial_id):

    stub = service_pb2_grpc.StudentServiceStub(channel)

    request = service_pb2.StudentUpdatePaymentIdRequest(
        student_id = student_id,
        financial_id = financial_id,
    )

    response = stub.UpdateStudentPaymentId(request)

    response_dict = {
        "success" : response.success
    }

    return response_dict

def delete_student_by_id(student_id):

    stub = service_pb2_grpc.StudentServiceStub(channel)

    request = service_pb2.StudentDeleteRequest(
        student_id = student_id,
    )

    response = stub.DeleteStudentById(request)

    response_dict = {
        "success" : response.success
    }

    return response_dict

def get_student_by_name(name):

    stub = service_pb2_grpc.StudentServiceStub(channel)

    request = service_pb2.StudentSearchRequest(
        student_name = name,
    )

    response = stub.GetStudentByName(request)

    students_list = []

    for student in response.student:
        student_data = {
            "id": student.id,
            "name": student.name,
            "gender": get_gender_by_id(student.gender_id),
            "birthday": student.birthday,
            "email": student.email,
            "phone": student.phone,
            "state": get_state_by_id(student.state_id),
            "city": student.city,
            "neighborhood": student.neighborhood,
            "address": student.address,
            "number": student.number,
            "cep": student.cep,
            "payment": get_payment_info(student.id),
            "nivel": get_nivel_by_id(student.nivel_id),
            "goal": get_goal_by_id(student.goal_id)
        }
        students_list.append(student_data)

    return jsonify(students_list)




