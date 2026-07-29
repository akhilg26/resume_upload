import { useState } from 'react'
import { useNavigate, Link } from 'react-router-dom'


const API_URL = 'http://localhost:8000' // check slash

function Upload(){
    const [resumeText, setResumeText] = useState('')
    const [jobText, setJobText] = useState('')
    const [loading, setLoading] = useState(false)
    const [error, setError] = useState('')
    const [resumeId, setResumeId] = useState(0)
    const [jobId, setJobId] = useState(0)
    const [matchScore, setMatchScore] = useState(0)
    const navigate = useNavigate()

    async function handleSubmit(e, endpoint, text){ // mess with url parameters to avoid duplication
        e.preventDefault()
        const token = localStorage.getItem('token')
        if (!token){
            setError('You must be logged in')
            return
        }

        setLoading(true)
        try {const res = await fetch(`${API_URL}/${endpoint}`, {
            method: 'POST', headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json'
            }, body: JSON.stringify({rawtext: text}),
        })
        const data = await res.json()
        if (!res.ok) {
            setError(data.detail || 'Upload failed')
        }

        if (endpoint === 'resumes'){
            setResumeId(data.resume_id)
        } else {
            setJobId(data.job_id)
        }
        
    } catch (err) {
        setError('Could not reach server')
    } finally {
        setLoading(false)
    }

    }

    async function calculateScore(e){
        e.preventDefault()
        const token = localStorage.getItem('token')
        if (!token){
            setError('You must be logged in')
            return
        }
        setLoading(true)
        try {
            const res = await fetch(`${API_URL}/match`, {
                method: 'POST', headers: {'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'}, body: JSON.stringify({resume_id: resumeId, job_id: jobId})
            })
            const data = await res.json()
            setMatchScore(data.score)
        } catch (err) {
            setError('Could not reach server')
            return
        } finally {
            setLoading(false)
        }
        
    }
    
    // add css styling headers later
    return <div style={{display: 'flex', justifyContent: 'center', flexDirection: 'row', alignItems: 'center', gap: '100px'}}> 
            <div>
            <form onSubmit={(e) => handleSubmit(e, 'resumes', resumeText)}>

            <label for="resume">Resume</label> <br />
            <textarea placeholder="Copy and paste resume" value={resumeText} onChange={e => setResumeText(e.target.value)}></textarea> <br />

            <button type='submit' disabled={loading}>Submit</button>
            </form>
            </div>
            <div>
            <form onSubmit={(e) => handleSubmit(e, 'jobs', jobText)}>
            <label for="job">Job Description</label> <br />
            <textarea placeholder="Copy and paste job description" value={jobText} onChange={e => setJobText(e.target.value)}></textarea> <br />
            <button type='submit' disabled={loading}>Submit</button>
            </form>
            </div>

            {resumeText && jobText ? <div>
                <form onSubmit={(e) => calculateScore(e)}>
                    <button style={{alignItems: 'center'}} type='submit' disabled={loading}>Calculate Score</button>
                </form>
            </div> : null}

            {matchScore !== 0 ? <div>{matchScore}</div> : null}
            
            
    </div>
}

export default Upload