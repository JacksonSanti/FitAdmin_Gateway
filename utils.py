from redis_client import get_token_by_email
from client_user import *
from client_financial import *
from jinja2 import Template
from weasyprint import HTML
from io import BytesIO
from datetime import datetime

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

def format_general_name(name):
    
    goal_name_map = {
        "hipertrofia": "Hipertrofia",
        "definicao": "Definição",
        "forca": "Força",
        "postura": "Postura",
        "estetica": "Estética",
        "condicionamento": "Condicionamento",
        "funcionalidade": "Funcionalidade",
        "resistencia": "Resistência",
        "superacao": "Superação",
        "comunidade": "Comunidade",
        "emagrecimento": "Emagrecimento",
        "cardio": "Cardio",
        "bem estar": "Bem-estar",
        "coordenacao": "Coordenação",
        "diversao": "Diversão",
        "reabilitacao": "Reabilitação",
        "correcao": "Correção",
        "mobilidade": "Mobilidade",
        "prevencao": "Prevenção",
        "recuperacao": "Recuperação",
        "iniciante": "Iniciante",
        "intermediario": "Intermediário",
        "avancado": "Avançado"
    }

    return goal_name_map.get(name.lower(), name)

def unformat_general_name(name):

    goal_name_map = {
        "hipertrofia": "Hipertrofia",
        "definicao": "Definição",
        "forca": "Força",
        "postura": "Postura",
        "estetica": "Estética",
        "condicionamento": "Condicionamento",
        "funcionalidade": "Funcionalidade",
        "resistencia": "Resistência",
        "superacao": "Superação",
        "comunidade": "Comunidade",
        "emagrecimento": "Emagrecimento",
        "cardio": "Cardio",
        "bem estar": "Bem-estar",
        "coordenacao": "Coordenação",
        "diversao": "Diversão",
        "reabilitacao": "Reabilitação",
        "correcao": "Correção",
        "mobilidade": "Mobilidade",
        "prevencao": "Prevenção",
        "recuperacao": "Recuperação",
        "musculacao": "Musculação",
        "crossfit": "CrossFit",
        "zumba": "Zumba",
        "fisioterapia": "Fisioterapia",
        "iniciante": "Iniciante",
        "intermediario": "Intermediário",
        "avancado": "Avançado"
    }

    return goal_name_map.get(name, name)

def generate_pdf_to_download(ai_data: dict, name, plan, nivel, goal):

    template = Template(open("template.html", encoding="utf-8").read())

    date_now = datetime.now()

    today = date_now.strftime("%d/%m/%Y")

    data = {
        "exercise": ai_data,
        "student": name,
        "plan": plan,
        "nivel": nivel,
        "goal": goal,
        "today": today
    }

    html_output = template.render(data) 

    pdf_bytes = HTML(string=html_output).write_pdf()

    return BytesIO(pdf_bytes) 
    