import datetime


def getAndFormatDataSaveS3(*args, **kwargs):
    today = (datetime.datetime.now()).strftime('%Y%m%d')
    print(today)

