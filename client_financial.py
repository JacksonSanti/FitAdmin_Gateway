import grpc
import service_pb2
import service_pb2_grpc
import json

channel = grpc.insecure_channel("user_grpc:50052")

def get_payment_by_id(user_id):

    stub = service_pb2_grpc.PaymentServiceStub(channel)

    request = service_pb2.PaymentRequest(user_id = user_id)

    response = stub.GetPaymentData(request)

    json_data = json.dumps(response, indent=4)

    return json_data

def get_plan_by_id(user_id):

    stub = service_pb2_grpc.PlanServiceStub(channel)

    request = service_pb2.PlanRequest(user_id = user_id)

    response = stub.GetPlanData(request)

    json_data = json.dumps(response, indent=4)

    return json_data