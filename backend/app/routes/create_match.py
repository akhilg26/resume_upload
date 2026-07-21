from fastapi import APIRouter, Depends, HTTPException
from dotenv import load_dotenv
from app.dependencies import verify_token
import os
import psycopg2
from app.models.match import Match
import numpy as np
import ast

load_dotenv()
router = APIRouter()
db_connection = os.getenv('SUPABASE')

@router.post('/match')
def match(match: Match, user_id: int = Depends(verify_token)):
    conn = psycopg2.connect(db_connection)
    cursor = conn.cursor()

    cursor.execute('SELECT embedding FROM resumes WHERE id = %s AND user_id = %s', (match.resume_id, user_id))
    result = cursor.fetchone()
    cursor.execute('SELECT embedding FROM job_descriptions WHERE id = %s AND user_id = %s', (match.job_id, user_id))
    result1 = cursor.fetchone()
    if result is None or result1 is None:
            raise HTTPException(
                status_code=404,
                detail='Job/resume not found'
            )

    resume_embedding_string = result[0]
    job_embedding_string = result1[0]
    resume_embedding = np.array(ast.literal_eval(resume_embedding_string))
    job_embedding = np.array(ast.literal_eval(job_embedding_string))
    dot_product = np.dot(resume_embedding, job_embedding)
    magnitude = np.linalg.norm(resume_embedding) * np.linalg.norm(job_embedding)
    cos_similarity = dot_product / magnitude
    score = round(cos_similarity * 100, 2)


    cursor.execute('INSERT INTO matches (resume_id, job_id, score) VALUES (%s, %s, %s) RETURNING id', (match.resume_id, match.job_id, score))
    result = cursor.fetchone()
    conn.commit()
    return {'message': 'Success',
            'match_id': result[0]}

