from dotenv import load_dotenv
import os
from sqlmodel import create_engine, Session


# load_dotenv()


# url = os.getenv('DATABASE_URI')


# engine = create_engine(url, echo=True)
engine = create_engine(
    "postgresql://edbqpqgpzyumgs:41c4a5f9d1f4e7345649cb25046bfaf5f3f9cef4a75321c970b6be70f139ac9a@ec2-52-201-124-168.compute-1.amazonaws.com:5432/dal3la68nt4bsb", echo=True)
