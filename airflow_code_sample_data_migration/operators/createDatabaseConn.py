import os
from airflow import settings
from airflow.models import Connection






def updateOperators(*args, **kwargs):
    analytics_staging_db = Connection(
        conn_id="analytics_staging_db",
        conn_type="postgres",
        host="host.docker.internal",
        schema="analytics_staging_db",
        login=os.environ["POSTGRES_USER"],
        password=os.environ["POSTGRES_PASSWORD"],
        port=os.environ["DB_Port"]
    )

    dev_staging_db = Connection(
        conn_id="dev_staging_db",
        conn_type="postgres",
        host="host.docker.internal",
        schema="dev_staging_db",
        login=os.environ["POSTGRES_USER"],
        password=os.environ["POSTGRES_PASSWORD"],
        port=os.environ["DB_Port"]
    )

    prod_db = Connection(
        conn_id="production_db",
        conn_type="postgres",
        host="host.docker.internal",
        schema="production_db",
        login=os.environ["POSTGRES_USER"],
        password=os.environ["POSTGRES_PASSWORD"],
        port=os.environ["DB_Port"]
    )
    session = settings.Session() # get the session
    session.add(analytics_staging_db)
    session.add(dev_staging_db)
    session.add(prod_db)
    session.commit() # it will insert the connection object programmatically.


