from redis_client import get_token_by_email
from client_user import *
from client_financial import *
from jinja2 import Template
from weasyprint import HTML
from io import BytesIO
from datetime import datetime

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
    