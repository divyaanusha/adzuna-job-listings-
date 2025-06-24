docker compose up -d
docker compose start -d

docker exec -it weather-etl-postgres-1  /bin/bash
/var/lib/postgresql/data# psql -U airflow -d airflow
