import os

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-key-change-me")
    # Usa .env si está; si no, por defecto va a MySQL local con miniblog_user sin password
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL",
        "mysql+pymysql://miniblog_user:@localhost/miniblog?charset=utf8mb4"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
