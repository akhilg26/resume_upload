import os
from dotenv import load_dotenv
import psycopg2

load_dotenv()

db_connection = os.getenv('SUPABASE')

def get_connection():
    return psycopg2.connect(db_connection)