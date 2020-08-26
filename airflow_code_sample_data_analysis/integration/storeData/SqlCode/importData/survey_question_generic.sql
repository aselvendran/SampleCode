COPY athavan.table_name from 's3://aws_bucket/surveyData/table_name/ds=date_loaded/data.csv'
    access_key_id 'aws_access_key'
    secret_access_key 'aws_secret_key'
    region 'us-east-1'
    ignoreheader 1
    null as 'NA'
    removequotes
    EMPTYASNULL
    BLANKSASNULL
    TRIMBLANKS
    IGNOREBLANKLINES
    delimiter ','
    DATEFORMAT AS 'MM/DD/YYYY'
    MAXERROR 10