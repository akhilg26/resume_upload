from fastapi import APIRouter, Depends
from app.models.document import DocumentModel
import psycopg2
from dotenv import load_dotenv
import os
from app.dependencies import verify_token

load_dotenv()

db_connection = os.getenv('SUPABASE')


router = APIRouter()

@router.post('/resumes')
def resume_upload(resume: DocumentModel, user_id: int = Depends(verify_token)):
    conn = psycopg2.connect(db_connection)
    cursor = conn.cursor()
    cursor.execute('INSERT INTO resumes (user_id, raw_text, embedding) VALUES (%s, %s, %s) RETURNING id', (user_id, resume.rawtext, 'placeholder'))
    result = cursor.fetchone()
    conn.commit()
    return {'message': 'SUCCESS',
            'resume_id': result[0]}

@router.post('/jobs')
def job_desc_upload(job: DocumentModel, user_id: int = Depends(verify_token)):
    conn = psycopg2.connect(db_connection)
    cursor = conn.cursor()
    cursor.execute('INSERT INTO job_descriptions (user_id, raw_text, embedding) VALUES (%s, %s, %s) RETURNING id', (user_id, job.rawtext, 'placeholder'))
    result = cursor.fetchone()
    conn.commit()
    return {'message': 'success!',
            'job_id': result[0]}

