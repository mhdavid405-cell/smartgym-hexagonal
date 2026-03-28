import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

load_dotenv()

class DatabaseConfig:
    def __init__(self):
        self.server = os.getenv('DB_HOST', 'localhost')
        self.database = os.getenv('DB_NAME', 'smartgym_db')
        self.username = os.getenv('DB_USER', 'sa')
        self.password = os.getenv('DB_PASSWORD', '')
    
    def get_connection_string(self):
        # Usar ODBC Driver 17 (instalado en el contenedor)
        return f"mssql+pyodbc://{self.username}:{self.password}@{self.server}/{self.database}?driver=ODBC+Driver+17+for+SQL+Server"
    
    def create_engine(self):
        return create_engine(self.get_connection_string())
    
    def get_session(self):
        engine = self.create_engine()
        Session = sessionmaker(bind=engine)
        return Session()