from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

import os
from dotenv import load_dotenv

load_dotenv()

# 환경변수에서 데이터베이스 연결 정보 가져오기
user = os.getenv('DB_USER', 'root')
passwd = os.getenv('DB_PASSWORD', '')
host = os.getenv('DB_HOST', 'localhost')
port = os.getenv('DB_PORT', '3306')
db = os.getenv('DB_NAME', 'user_db')

DB_URL = f'mysql+pymysql://{user}:{passwd}@{host}:{port}/{db}?charset=utf8'

engine = create_engine(DB_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
