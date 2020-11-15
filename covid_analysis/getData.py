import pandas as pd
import datetime
import boto3
import io
import gzip

df_columns = ['province_state', 'country_region', 'last_update', 'lat', 'long_',
              'confirmed', 'deaths', 'recovered', 'active', 'fips', 'incident_rate',
              'people_tested', 'people_hospitalized', 'mortality_rate', 'uid', 'iso3',
              'testing_rate', 'hospitalization_rate']


class S3Connection:
    def __init__(self, aws_bucket, aws_access_key, aws_secret_key):
        self.aws_bucket = aws_bucket
        self.aws_access_key = aws_access_key
        self.aws_secret_key = aws_secret_key
        self.session = boto3.Session(
            aws_access_key_id=self.aws_access_key,
            aws_secret_access_key=self.aws_secret_key,
            region_name='us-east-2'
        )

        self.client = boto3.client('s3',
                                   aws_access_key_id=aws_access_key,
                                   aws_secret_access_key=aws_secret_key
                                   )

    def pandasToS3(self, df, fileName):
        # write DF to string stream
        csv_buffer = io.StringIO()
        df.to_csv(csv_buffer, index=False, header=False)

        # reset stream position
        csv_buffer.seek(0)
        # create binary stream
        gz_buffer = io.BytesIO()

        # compress string stream using gzip
        with gzip.GzipFile(mode='w', fileobj=gz_buffer) as gz_file:
            gz_file.write(bytes(csv_buffer.getvalue(), 'utf-8'))

        # write stream to S3
        self.client.put_object(Bucket=self.aws_bucket, Key=fileName, Body=gz_buffer.getvalue())


access_key = ""
secret_key = ""

s3Connection = S3Connection("aws_bucket", access_key, secret_key)


def addColumn(data, column):
    data[column] = None


def getData(date_to_load):
    format_str = '%m-%d-%Y'
    daytime_ = datetime.datetime.strptime(date_to_load, format_str)
    url_to_data = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports_us/%s.csv' % date_to_load
    raw_data = pd.read_csv(url_to_data)
    raw_data.columns = [column.lower() for column in raw_data.columns]
    [addColumn(raw_data, column_to_add) for column_to_add in df_columns if column_to_add not in raw_data.columns]

    raw_data = raw_data[df_columns]
    filename = r'compressed/country=US/year=%s/month=%s/day=%s/state={}/data.txt.gz' % (
        daytime_.year, daytime_.month, daytime_.day)

    raw_data.groupby(['province_state'], as_index=False).apply(
        lambda data_: s3Connection.pandasToS3(data_.drop(['province_state', 'country_region'], axis=1),
                                              filename.format(data_.name)))


def backFillData(start_date, end_date):
    list_of_dates = [date.strftime("%m-%d-%Y") for date in pd.date_range(start=start_date, end=end_date)]
    [getData(date_) for date_ in list_of_dates]


# backFillData("04-12-2020","08-24-2020")

