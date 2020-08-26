from airflow_code_sample_data_analysis.integration.formatData.surveyData import formatData
from airflow_code_sample_data_analysis.integration.storeData.saveDataFunctions import s3RedshiftConn
import configparser
from pathlib import Path

config = configparser.ConfigParser()
import os, sys

rootUserPath = os.getcwd().split("survey_analysis")[0] + "/survey_analysis"
sys.path.append(rootUserPath)

os.chdir(rootUserPath)
config.read('integration/config.ini')

s3RedshiftConn = s3RedshiftConn(aws_access_key=config['Aws']['accessKey'],
                                aws_secret_key=config['Aws']['secretKey'], aws_bucket="",
                                redshift_username=config['RedShift']['userName'],
                                redshift_password=config['RedShift']['password'],
                                redshift_database=config['RedShift']['dataBase'],
                                redshift_host=config['RedShift']['host'])


def saveAllTablesToS3(date_loaded):
    """

    This method saves all survey questions into s3.

    @return: None. saves data to s3.

    """
    fmtData = formatData()

    userData = fmtData.getUserData()

    lesuireData = fmtData.getLesiureData()[0]
    lesuireData['question'] = "question_1"

    lesuireDataOther = fmtData.getLesiureData()[1]
    lesuireDataOther['question'] = "question_1"

    businessData = fmtData.getBusinessData()[0]
    businessData['question'] = "question_2"

    businessDataOther = fmtData.getBusinessData()[1]
    businessDataOther['question'] = "question_2"

    genderData = fmtData.getGenderData()[0]
    genderData['question'] = "question_3"

    genderDataOther = fmtData.getGenderData()[1]
    genderDataOther['question'] = "question_3"

    cityData = fmtData.getCityEnerData()
    cityData['question'] = "question_4"

    ageData = fmtData.getAgeData()
    ageData['question'] = "question_5"

    considerationData = fmtData.getConsiderationData()
    considerationData['question'] = "question_6"

    surveyColumnData = fmtData.getSurveyColumns()

    dataToSave = [
        ("user_data",userData),
        ("lesuire_data", lesuireData), ("lesuire_data_other", lesuireDataOther),
        ("business_data", businessData), ("business_data_other", businessDataOther),
        ("gender_data", genderData), ("gender_data_other", genderDataOther), ("city_data", cityData),
        ("age_data", ageData), ("consideration_data", considerationData), ("survey_question", surveyColumnData)]

    [s3RedshiftConn.saveDfToS3(data[1], "surveyData/%s/ds=%s" % (data[0], date_loaded)) for data in dataToSave]


def createRedshiftTable(table_name):
    """

    This method creates tables in Redshift

    @return: None. table created in redshift.

    """

    importDataFolder = Path("integration/storeData/SqlCode/createTable/")
    fileToOpen = importDataFolder / ("%s.sql" % "survey_question_generic")
    fileToImport = open(fileToOpen, 'r')
    sqlScript = fileToImport.read().replace("table_name", table_name)
    s3RedshiftConn.executeRedshiftScript(sqlScript)


def copyDataToRedshift(table_name, date_loaded):
    """

    This method copies data into Redshift

    @return: None. method copies data into Redshift

    """
    print("this is the check", os.getcwd())
    importDataFolder = Path("integration/storeData/SqlCode/importData/")
    fileToOpen = importDataFolder / ("%s.sql" % "survey_question_generic")
    fileToImport = open(fileToOpen, 'r')
    sqlScript = fileToImport.read().replace("table_name", table_name).replace("aws_access_key",
                                                                              s3RedshiftConn.aws_access_key).replace(
        "aws_secret_key", s3RedshiftConn.aws_secret_key).replace("aws_bucket", s3RedshiftConn.aws_bucket).replace(
        "date_loaded", date_loaded)
    s3RedshiftConn.executeRedshiftScript(sqlScript)


def createSurveyQuestionTableAndImport(date_loaded):
    tableToCreate = "survey_question"

    createRedshiftTable(tableToCreate)
    copyDataToRedshift(tableToCreate, date_loaded)


def createAllTables():
    """

    This method creates tables for all the survey Questions as well as the user data.

    @return: None.

    """

    tableListSurveyQuestionsToCreate = ["lesuire_data", "lesuire_data_other", "business_data", "business_data_other",
                                        "gender_data",
                                        "gender_data_other",
                                        "city_data", "age_data", "consideration_data"]

    [createRedshiftTable(table) for table in tableListSurveyQuestionsToCreate]
    userDataTable = "user_data"
    createRedshiftTable(userDataTable)


def copyAllDataToRedshift(date_loaded):
    """

    This method loads survey data and user data  from s3 to Redshift.

    @return: None.

    """

    tableListSurveyQuestionsToImport = ["lesuire_data", "lesuire_data_other", "business_data", "business_data_other",
                                        "gender_data",
                                        "gender_data_other",
                                        "city_data", "age_data", "consideration_data"]
    [copyDataToRedshift(table, date_loaded) for table in tableListSurveyQuestionsToImport]

    userDataTable = "user_data"
    copyDataToRedshift(userDataTable, date_loaded)


