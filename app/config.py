# app/config.py

class Config:
    SECRET_KEY = 'your_secret_key'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///your_database.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False


# # Configuración de la aplicación
# class Config:
#     SECRET_KEY = 'your_secret_key'
#     SQLALCHEMY_DATABASE_URI = 'sqlite:///example.db'
#     SQLALCHEMY_TRACK_MODIFICATIONS = False