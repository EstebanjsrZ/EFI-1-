import os

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-key-change-me")
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL",
        "mysql+pymysql://miniblog_user:@localhost/miniblog?charset=utf8mb4"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
