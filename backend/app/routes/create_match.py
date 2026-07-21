from fastapi import APIRouter, Depends, HTTPException
from dotenv import load_dotenv
from app.dependencies import verify_token
import os
import psycopg2
from models.match import Match

load_dotenv()
router = APIRouter()
db_connection = os.getenv('SUPABASE')

@router.post('/match')
def match(match: Match, user_id: int = Depends(verify_token)):
    conn = psycopg2.connect(db_connection)
    cursor = conn.cursor()

    cursor.execute('SELECT embedding FROM resumes WHERE id = %s AND user_id = %s', (match.resume_id, user_id))
    result = cursor.fetchone()
    if result is None:
        raise HTTPException(
            status_code=404,
            detail='Resume not found; most likely that user_id does not match with resume'
        )

    cursor.execute('INSERT INTO matches (resume_id, job_id, score) VALUES (%s, %s, %s) RETURNING id', (match.resume_id, match.job_id, 100))
    result = cursor.fetchone()
    conn.commit()
    return {'message': 'Success',
            'match_id': result[0]}

