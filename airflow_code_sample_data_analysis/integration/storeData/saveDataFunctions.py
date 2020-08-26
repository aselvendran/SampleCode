from io import StringIO
import psycopg2
import boto3


class s3RedshiftConn:
    def __init__(self, aws_access_key, aws_secret_key, aws_bucket,
                 redshift_username, redshift_password, redshift_database, redshift_host):
        self.aws_access_key = aws_access_key
        self.aws_secret_key = aws_secret_key
        self.aws_bucket = aws_bucket
        self.redshift_username = redshift_username
        self.redshift_password = redshift_password
        self.redshift_database = redshift_database
        self.redshift_host = redshift_host
        self.session = boto3.Session(
            aws_access_key_id=self.aws_access_key,
            aws_secret_access_key=self.aws_secret_key,
            region_name='us-east-1'
        )

    def saveDfToS3(self, data_frame,
                   directory_to_save):
        """
        This method will take a DataFrame and save it to the according directory with a given file
        name.

        @param data_frame: The Data Frame that we hope to save
        @param directory_to_save: The directory to which the dataFrame will be saved to
        @return: None will be returned as we are pushing the dataframe to S3.
        """

        csvBuffer = StringIO()
        data_frame.to_csv(csvBuffer, index=False, header=True)
        content = csvBuffer.getvalue()

        s3 = self.session.resource('s3')

        object = s3.Object(self.aws_bucket, "%s/data.csv" % directory_to_save)
        object.put(Body=content)

    def executeRedshiftScript(self, sqlScript):
        """
        This method will execute a script in Redshift.

        @param sqlScript: The sql script in which you want to run in jdbc driver for redshift.
        @return: None will be returned as we are creating/importing data from s3 to redshift.

        """

        conn = psycopg2.connect(database=self.redshift_database, user=self.redshift_username,
                                password=self.redshift_password,
                                host=self.redshift_host, port="5432")
        cur = conn.cursor()
        print(sqlScript)
        cur.execute(sqlScript)
        conn.commit()
