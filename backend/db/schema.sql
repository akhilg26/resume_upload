CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE users(
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT now() 
);

CREATE TABLE resumes(
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id),
    raw_text TEXT NOT NULL,
    embedding vector(1536),
    created_at TIMESTAMP DEFAULT now()
);

CREATE TABLE job_descriptions(
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id),
    raw_text TEXT NOT NULL,
    embedding vector(384),
    created_at TIMESTAMP DEFAULT now()
);

CREATE TABLE matches(
    id SERIAL PRIMARY KEY,
    resume_id INTEGER NOT NULL REFERENCES resumes(id),
    job_id INTEGER NOT NULL REFERENCES job_descriptions(id),
    score FLOAT,
    created_at TIMESTAMP DEFAULT now()
);

CREATE TABLE match_skills(
    id SERIAL PRIMARY KEY,
    match_id INTEGER NOT NULL REFERENCES matches(id),
    skill TEXT NOT NULL,
    status TEXT NOT NULL CHECK (status IN ('matched', 'missing')) 
);