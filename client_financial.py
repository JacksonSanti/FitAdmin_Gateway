from flask import jsonify
import grpc
import service_pb2
import service_pb2_grpc
import json

channel = grpc.insecure_channel("financial_grpc:50052")

def get_payment_by_id(payment_id):

    stub = service_pb2_grpc.PaymentServiceStub(channel)

    request = service_pb2.PaymentRequestById(payment_id=payment_id)

    response = stub.GetPaymentDataById(request)

    response_dict = {
        "id": response.id,
        "user_id": response.user_id,
        "plan_id": response.plan_id,
        "method_id": response.method_id,
    }
    
    return json.dumps(response_dict, indent=4)

def get_payment():

    stub = service_pb2_grpc.PaymentServiceStub(channel)

    request = service_pb2.PaymentRequest()

    response = stub.GetPaymentData(request)

    payment_list = []

    for payment in response.payment:
        payment_data = {
        "id": payment.id,
        "user_id": payment.user_id,
        "plan_id": payment.plan_id,
        "method_id": payment.method_id,
        }

        payment_list.append(payment_data)

    return jsonify(payment_list)

def get_plan_by_id(plan_id):

    stub = service_pb2_grpc.PlanServiceStub(channel)

    request = service_pb2.PlanRequestById(plan_id = plan_id)

    response = stub.GetPlanDataById(request)

    response_dict = {
        "id": response.id,
        "name": response.name,
        "value": response.value,
    }

    return json.dumps(response_dict, indent=4)

def get_plan():

    stub = service_pb2_grpc.PlanServiceStub(channel)

    request = service_pb2.PlanRequest()

    response = stub.GetPlanData(request)

    plans_list = [
        {
            "id": plan.id,
            "name": plan.name,
            "value": plan.value 
        }
        for plan in response.plan
    ]

    return plans_list

def get_method_by_id(method_id):

    stub = service_pb2_grpc.MethodServiceStub(channel)

    request = service_pb2.MethodRequestById(method_id = method_id)

    response = stub.GetMethodDataById(request)

    response_dict = {
        "id": response.id,
        "name": response.name,
        "discount": response.discount,
    }

    return json.dumps(response_dict, indent=4)

def get_method():

    stub = service_pb2_grpc.MethodServiceStub(channel)

    request = service_pb2.MethodRequest()

    response = stub.GetMethodData(request)

    methods_list = [
        {
            "id": method.id,
            "name": method.name,
            "discount": method.discount
        }
        for method in response.method
    ]

    return methods_list

def get_payment_info(payment_id):

    payment = get_payment_by_id(int(payment_id))

    payemnt_json = json.loads(payment)

    method = get_method_by_id(int(payemnt_json['method_id']))

    method_json = json.loads(method)

    plan = get_plan_by_id(int(payemnt_json['plan_id']))

    plan_json = json.loads(plan)

    payment_dict =  {
        "method_id": method_json['id'],
        "method_name": method_json['name'],
        "method_discount": method_json['discount'],
        "plan_id": plan_json['id'],
        "plan_name": plan_json['name'],
        "plan_value": plan_json['value'],
        "payment_id" : payemnt_json['id'],
    }

    return payment_dict

def update_payment(payment_id,id,plan,method_id):
 
    stub = service_pb2_grpc.PaymentServiceStub(channel)

    request = service_pb2.PaymentResponse(
        id = payment_id,
        user_id = id,
        plan_id = plan,
        method_id = method_id
    )

    response = stub.UpdatePaymentData(request)

    response_dict = {
        "status" : response.success
    }

    return response_dict

def create_payment(id,plan,method_id):

    stub = service_pb2_grpc.PaymentServiceStub(channel)

    request = service_pb2.PaymentCreateRequest(
        user_id = id,
        plan_id = plan,
        method_id = method_id
    )

    response = stub.CreatePaymentData(request)

    response_dict = {
        "id" : response.id
    }

    return response_dict

def update_student_id_by_financial_id(student_id, financial_id):

    stub = service_pb2_grpc.PaymentServiceStub(channel)

    request = service_pb2.PaymentUpdateStudentIdRequest(
        student_id = student_id,
        financial_id = financial_id,
    )

    response = stub.UpdatePaymentStudentId(request)

    response_dict = {
        "success" : response.success
    }

    return response_dict

def delete_payment_by_id(payment_id):

    stub = service_pb2_grpc.PaymentServiceStub(channel)

    request = service_pb2.PaymentDeleteRequest(
        payment_id = payment_id,
    )

    response = stub.DeletePaymentById(request)

    response_dict = {
        "success" : response.success
    }

    return response_dict