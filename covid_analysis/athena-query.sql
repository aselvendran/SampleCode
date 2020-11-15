-- Create a database in athena
CREATE DATABASE covid;

-- Create table with all the data from github pull
CREATE EXTERNAL TABLE IF NOT EXISTS covid.logs_partitioned (
  last_update string,
  lat double,
  long_ double,
  confirmed double,
  deaths double,
  recovered double,
  active double,
  fips double,
  incident_rate double,
  people_tested double,
  people_hospitalized double,
  mortality_rate double,
  uid bigint,
  iso3 string,
  testing_rate double,
  hospitalization_rate double
   )

PARTITIONED BY (country string, year int ,month int, day int,state string)

row format delimited fields terminated by ','
stored as inputformat 'org.apache.hadoop.mapred.TextInputFormat'
outputformat 'org.apache.hadoop.hive.ql.io.HiveIgnoreKeyTextOutputFormat'

LOCATION 's3://aws_bucket/compressed/';

-- Repair the partitions
MSCK REPAIR TABLE covid.logs_partitioned;


-- Query for Viz


CREATE TABLE covid.tableau_viz
WITH ( format='JSON', external_location='s3://aws_bucket/results_', bucket_count = 1, bucketed_by=ARRAY['state'] ) AS
SELECT state,
         (cast(month AS VARCHAR) || '/' || cast(day AS VARCHAR) || '/2020') AS date_loaded,

         recovered - lag( recovered , 1 )
    OVER ( PARTITION BY state
ORDER BY  year,month,day) AS recovered_time_series,


deaths - lag( deaths , 1 )
    OVER ( PARTITION BY state
ORDER BY  year,month,day) AS deaths_time_series,


confirmed - lag( confirmed , 1 )
    OVER ( PARTITION BY state
ORDER BY  year,month,day) AS confirmed_time_series,

people_tested - lag( people_tested , 1 )
    OVER ( PARTITION BY state
ORDER BY  year,month,day) AS people_tested_time_series,
    CASE
    WHEN (people_tested - lag( people_tested , 1 )
    OVER ( PARTITION BY state
ORDER BY  year,month,day)) < 0 THEN
    'BAD DATA'
    ELSE ''
    END AS health_check
FROM covid.logs_partitioned