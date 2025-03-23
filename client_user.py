import grpc
import service_pb2
import service_pb2_grpc
import json
from client_financial import *

channel = grpc.insecure_channel("user_grpc:50051")

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

        students_list = [
            {
                "id": student.id,
                "name": student.name,
                "gender_id": student.gender_id,
                "birthday": student.birthday,
                "email": student.email,
                "phone": student.phone,
                "state_id": student.state_id,
                "city": student.city,
                "neighborhood": student.neighborhood,
                "address": student.address,
                "number": student.number,
                "plan_id": student.plan_id,
                "payment_id": student.payment_id,
            }
            for student in response.student
        ]


        json_data = json.dumps(students_list, indent=4) 
    
        return json_data 

    except grpc.RpcError as e:

        return {"error": f"Erro ao buscar estudantes: {e.details()}"}

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


    json_data = json.dumps(states_list, indent=4)

    return json_data

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

    json_data = json.dumps(gender_list, indent=4)

    return json_data


