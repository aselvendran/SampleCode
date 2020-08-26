from airflow_code_sample_data_analysis.integration.dailyWorkFlow.surveyData import *
import datetime


def getAndFormatDataSaveS3(*args, **kwargs):
    today = (datetime.datetime.now()).strftime('%Y%m%d')
    saveAllTablesToS3(today)


def loadDataToS3(*args, **kwargs):
    today = (datetime.datetime.now()).strftime('%Y%m%d')
    copyAllDataToRedshift(today)
