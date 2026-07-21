from fastapi import APIRouter, Depends
from app.models.document import DocumentModel
from app.dependencies import verify_token
from sentence_transformers import SentenceTransformer
from db.connection import get_connection

router = APIRouter()
model = SentenceTransformer('all-MiniLM-L6-v2')

@router.post('/resumes')
def resume_upload(resume: DocumentModel, user_id: int = Depends(verify_token)):
    embedding = model.encode(resume.rawtext) #np array
    embedding_list = embedding.tolist() # python list
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO resumes (user_id, raw_text, embedding) VALUES (%s, %s, %s) RETURNING id', (user_id, resume.rawtext, str(embedding_list))) # psycopg2 can't convert python list or np array into SQL formats, python str of list of vectors converts to SQL string easier
    result = cursor.fetchone()
    conn.commit()
    return {'message': 'SUCCESS',
            'resume_id': result[0]}

@router.post('/jobs')
def job_desc_upload(job: DocumentModel, user_id: int = Depends(verify_token)):
    embedding = model.encode(job.rawtext)
    embedding_list = embedding.tolist()
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO job_descriptions (user_id, raw_text, embedding) VALUES (%s, %s, %s) RETURNING id', (user_id, job.rawtext, str(embedding_list)))
    result = cursor.fetchone()
    conn.commit()
    return {'message': 'success!',
            'job_id': result[0]}

