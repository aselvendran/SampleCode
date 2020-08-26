import pandas as pd
import os, sys

rootUserPath = os.getcwd().split("airflow")[0]
sys.path.append(rootUserPath)


class SurveyData:
    def __init__(self):
        pass

    def getData(self) -> pd.DataFrame:
        """
        This method will retrieve the survey data which is currently living in the parent directory.
        Ths method can be an api call, s3 read, ftp read etc.

        @return: Pandas Dataframe with the survey data, removing the first row which seems to be a placeholder row.

        """

        rawData = pd.read_csv('integration/fictional_survey.csv')
        rawData = rawData.rename(columns={'Respondent ID': 'respondent_id'})
        rawData['respondent_id'] = rawData['respondent_id'].astype(str)
        rawData = rawData.iloc[1:]
        return rawData
