from fastapi import FastAPI, Depends, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import psycopg2
from fastapi import Request

app = FastAPI()

# Setup the Jinja2 template engine
templates = Jinja2Templates(directory="templates")

# PostgreSQL connection setup
def get_db_connection():
    conn = psycopg2.connect(
        dbname="airflow", user="airflow", password="airflow", host="postgres", port="5432"
    )
    return conn

# Model for the job listing
class JobListing(BaseModel):
    title: str
    company: str
    location: str
    url: str
    description: str

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT title, company, location, url, description, date_added FROM adzuna_job_listings ORDER BY date_added DESC;")
    jobs = cursor.fetchall()
    cursor.close()
    conn.close()
    
    # Convert the tuple data into a dictionary
    job_list = [
        {
            "title": job[0],
            "company": job[1],
            "location": job[2],
            "url": job[3],
            "description": job[4],
            "date_added": job[5],  # Add date_added field
        }
        for job in jobs
    ]
    
    # Render the HTML with the job data
    return templates.TemplateResponse("index.html", {"request": request, "jobs": job_list})

    
# API route to fetch job listings (for potential API integration)
@app.get("/api/jobs", response_model=list[JobListing])
async def get_jobs():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT title, company, location, url, description FROM adzuna_job_listings;")
    jobs = cursor.fetchall()
    cursor.close()
    conn.close()
    return [{"title": job[0], "company": job[1], "location": job[2], "url": job[3], "description": job[4]} for job in jobs]
