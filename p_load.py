import os
import atexit
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError


from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')

if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_DB = os.getenv("POSTGRES_DB")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_HOST = os.getenv("POSTGRES_HOST")

SQLALCHEMY_DATABASE_URI = f'postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:5432/{POSTGRES_DB}'

engine = create_engine(SQLALCHEMY_DATABASE_URI, client_encoding = 'utf-8')
Session = sessionmaker(bind=engine)

Base = declarative_base()

atexit.register(lambda:engine.dispose())

class HttpError(Exception):
    def __init__(self, status_code, error_message):
        self.status_code = status_code
        self.error_message = error_message

class CharStar(Base):
    __tablename__ = 'characters'
    id = Column(Integer, primary_key=True)
    birth_year = Column(String, nullable=False)
    eye_color = Column(String, nullable=False)
    films = Column(String, nullable=False)
    gender = Column(String, nullable=False)
    hair_color = Column(String, nullable=False)
    height = Column(String, nullable=False)
    homeworld = Column(String, nullable=False)
    mass = Column(String, nullable=False)
    name = Column(String, nullable=False, unique = True)
    skin_color = Column(String, nullable=False)
    species = Column(String, nullable=False)
    starships = Column(String, nullable=False)
    vehicles = Column(String, nullable=False)

Base.metadata.create_all(engine)

async def recording(data):
    with Session() as session:
        try:
            rec = CharStar(
            birth_year = data['birth_year'],
            eye_color = data['eye_color'],
            films = data['films'],
            gender = data['gender'],
            hair_color = data['hair_color'],
            height = data['height'],
            homeworld = data['homeworld'],
            mass = data['mass'],
            name = data['name'],
            skin_color = data['skin_color'],
            species = data['species'],
            starships = data['starships'],
            vehicles = data['vehicles']
            )

            session.add(rec)
            session.commit()
            return print(data['name'])

        except IntegrityError:
            raise HttpError(400, 'Character exists')



