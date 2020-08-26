cd /docker-entrypoint-initdb.d
psql -d production_db -U airflow -f 2-arcadia-mock-production-exercise.db




