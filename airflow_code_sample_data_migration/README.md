#### Airflow Assignment

The goal of this pipeline is to create a production like environment
where data from a Production Server can be funneled into a Staging cluster
for different roles/users within an organization. With that in mind; this templated
Airflow service can be scaled up to handle this challenge 
at hand. Below is the setup for  this project.
   
    ├── dags                                
    ├── operators                           
    ├── sql
    ├── docker-compose.yaml
    └── README.md
    
    sql -> contains all the sql scripts that I will be using. One set is to create filtered views for the staging tables 
    stored in Production. Another set of tables is to create tables in the staging database.
    
    dag -> Workflow for storing data into a Production Database; creating filtered views for the staging database and then
    migrating the data from the production schema into the corresponding staging schemas.

    operator -> The operator contains the connections to the local postgres Schemas.

    
 
    



#### Useful Docker Commands to run ETL

```bash

cd arcadia
docker-compose up

# Command to access interactive terminal
docker container ls -la
docker exec -it <container_id> /bin/bash


# Once the job is triggered and completed; can access the data via
# script below or through Data Profiling -> Ad Hoc Query
psql -d production_db -U airflow
psql -d analytics_staging_db -U airflow
psql -d dev_staging_db -U airflow
 
```


#### Postgres Databases and Tables 

```$xslt

For this assignment, I created three databases; one for production, one for development staging and one for analytics staging. 
The motivation behind this is the data will be used differently across this data universe. Analyst will use the data
 to find trends/reports and developers will use the data to develop a software. 
Since the needs are different for both groups; not all the columns and values have to be a one to one match.
For the viewers in Analytics; what he/she will need is the historical data on a user's behavior.
What the devloper viewers will need is a role that enables them to funnel data into whatever software he/she is working on; 
therefore the data can be hashed.   
With this in mind; there were several columns that I filtered for the Analyst Staging database and for the Developer database; 
I masked several columns since raw values are not needed for developers; placeholders are good enough. 


```


### Airflow Tasks

> `addDBConnections` -> Add connection id in airflow service for three databases we are creating. The databases are initialized 
once docker compose is triggered.

> `insert_analytics_staging_tb_snapshot & insert_dev_staging_tb_snapshot`  -> these tasks trigger sql scripts that create 
several views in the Production Database that will be migrated to the Staging database. 

> `create_tables_staging_dev & create_tables_staging_analytics` -> These tasks trigger sql scripts which create staging tables in the corresponding 
databases.

> `unload_data_into_analytics_staging_db & unload_data_into_cev_staging_db` -> Using a function built within the dag file; 
the module `psycopg2` is used to insert values from one database into another. 


#### Further Analysis


```$xslt
Next steps should include creating roles for each database and 
then assigning users to each role. Within each role; there should be limitation on what can be done within the database such as create/edit/update rows.
The role management can live outside of this current pipeline and can be maintained using psql.  

```