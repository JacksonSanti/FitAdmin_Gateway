from flask import Flask
from routes import gateway
from flask_cors import CORS
from datetime import timedelta
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, JWTManager

def create_app():

    app = Flask(__name__)

    CORS(app)

    app.config["JWT_SECRET_KEY"] = "82824313354f36de2ebd74a5cea8960ff6d66b6ad11187f7b981746d311a04df"
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=5)  
    app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=7) 

    JWTManager(app)

    app.register_blueprint(gateway, url_prefix='/')

    return app 