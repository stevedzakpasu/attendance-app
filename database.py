from dotenv import load_dotenv
import os
from sqlmodel import create_engine


load_dotenv()


url = os.getenv('DATABASE_URI')


# engine = create_engine(url, echo=True)
engine = create_engine(url, echo=True)
