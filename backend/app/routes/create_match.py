from fastapi import APIRouter
from dotenv import load_dotenv
import os
import psycopg2



router = APIRouter()
db_connection = os.getenv('SUPABASE')

@router.post('/match')
def match(resume_id, job_id):
    conn = psycopg2.connect(db_connection)
    cursor = conn.cursor()
    cursor.execute('INSERT INTO matches (resume_id, job_id, score) VALUES (%s, %s, %s) RETURNING id', (resume_id, job_id, 100))
    result = cursor.fetchone()
    conn.commit()
    return {'message': 'Success',
            'match_id': result[0]}

