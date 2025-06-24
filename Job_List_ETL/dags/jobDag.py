import requests
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
from airflow.providers.postgres.hooks.postgres import PostgresHook

# Define the Airflow DAG
default_args = {
    'owner': 'airflow',
    'retries': 1,
    'retry_delay': timedelta(minutes=1),
}

dag = DAG(
    'adzuna_api_to_postgresql',
    default_args=default_args,
    description='Extract Data Engineer jobs from Adzuna API and save to PostgreSQL',
    start_date=datetime(2025, 6, 24),
    schedule_interval='@daily',
    catchup=False,
)

# Create Table Task: This will run once to create the table if not already present
def create_table_in_postgres():
    hook = PostgresHook(postgres_conn_id='postgresql')  # Make sure the connection ID is correct
    create_table_sql = """
    CREATE TABLE IF NOT EXISTS adzuna_job_listings (
        id SERIAL PRIMARY KEY,
        title VARCHAR(255) NOT NULL,
        company VARCHAR(255),
        location VARCHAR(255),
        url TEXT UNIQUE NOT NULL,
        description TEXT,
        date_added TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        date_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """
    hook.run(create_table_sql)

# Function to fetch data from the Adzuna API
def fetch_adzuna_data():
    url = "https://api.adzuna.com/v1/api/jobs/us/search/2"
    params = {
        'app_id': '0c36c4c5',
        'app_key': '4037b7fa0dfe3a5cf5735a2f7ef8ca91',
        'results_per_page': 50,
        'what': 'Data Engineer',
        'where': 'dallas',
        'max_days_old': 1,
        'sort_by': 'date'
    }
    
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to fetch data: {response.status_code}")
        return None

# Function to save data to PostgreSQL
def save_to_postgresql(data):
    if data:
        hook = PostgresHook(postgres_conn_id='postgresql')
        insert_query = """
        INSERT INTO adzuna_job_listings (title, company, location, url, description, date_added, date_updated)
        VALUES (%s, %s, %s, %s, %s, %s, %s) ON CONFLICT (url) DO NOTHING;
        """

        # Loop through the data and insert each job posting into the database
        for job in data['results']:
            title = job.get('title', '')
            company = job.get('company', {}).get('display_name', '')
            location = job.get('location', {}).get('area', [''])[0]
            url = job.get('redirect_url', '')
            description = job.get('description', '')
            date_added = datetime.now()  # Current time for insertion
            date_updated = datetime.now()  # Current time for insertion

            # Execute the insert query
            hook.run(insert_query, parameters=(title, company, location, url, description, date_added, date_updated))

# Define the Airflow task to fetch and save data
def extract_and_save_data():
    data = fetch_adzuna_data()
    if data:
        save_to_postgresql(data)

# Define Airflow tasks
create_table_task = PythonOperator(
    task_id='create_table_in_postgres',
    python_callable=create_table_in_postgres,
    dag=dag,
)

fetch_and_save_task = PythonOperator(
    task_id='fetch_and_save_adzuna_data',
    python_callable=extract_and_save_data,
    dag=dag,
)

# Set task dependencies
create_table_task >> fetch_and_save_task


if __name__ == "__main__":
    dag.test()