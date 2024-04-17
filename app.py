from flask import Flask, jsonify
from flask_smorest import Api
import os
from db import db
import models
from resources.users import blp as UsersBluePrint

from flask_jwt_extended import JWTManager

def create_app(db_url = None):
    app = Flask(__name__)
    
    jwt = JWTManager(app)
    app.config["JWT_SECRET_KEY"] = "53135608477443997068995402425053148094"
    
    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return (
            jsonify({"message": "The token has expired.", "error": "token_expired"}),
            401,
        )

    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return (
            jsonify(
                {"message": "Signature verification failed.", "error": "invalid_token"}
            ),
            401,
        )

    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return (
            jsonify(
                {
                    "description": "Request does not contain an access token.",
                    "error": "authorization_required",
                }
            ),
            401,
        )
    
    app.config["PROPAGATE_EXCEPTIONS"] = True
    app.config["API_TITLE"] = "Stores REST API"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
    app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    app.config["SQLALCHEMY_DATABASE_URI"] = db_url or os.getenv("DATABASE_URL", "sqlite:///data.db") # use db_url argument if passed, else use database_url from environment variables or default to sqlite url
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app) # initializes flask-sqlalchemy extension

    api = Api(app)

    # Manually create an application context
    with app.app_context():
    # Now you have access to the application context
    # Perform actions that require the application context here
        db.create_all()  # This will create the database tables if they don't exist already

    api.register_blueprint(UsersBluePrint)
    return app

app = create_app()
