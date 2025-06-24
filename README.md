 docker ps -  check for containers
cd .\Job_Listings\
cd .\fastapi-app
docker compose up --build -  to build an image from docker file


cd .\Job_Listings\
docker compose up -d
docker compose start -d
docker compose down


docker exec -it weather-etl-postgres-1  /bin/bash
/var/lib/postgresql/data# psql -U airflow -d airflow
