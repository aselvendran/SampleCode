from airflow_code_sample_data_analysis.integration.getData.surveyData import SurveyData
import numpy as np
import pandas as pd


class formatData:
    def __init__(self):
        self.getSurveyData = SurveyData().getData()

    def getUserData(self):
        """
        This method will filter the survey data to only include the user information.

        @return: Pandas Dataframe with the user data.

        """

        rawData = self.getSurveyData
        rawData = rawData.rename(columns={'Start Date': 'start_data', 'End Date': 'end_date',
                                          'IP Address': 'ip_address',
                                          'Email Address': 'email_address',
                                          'First Name': 'first_name',
                                          'Last Name': 'last_name'})
        return rawData[
            ["respondent_id", "start_data", "end_date", "ip_address", "email_address", "first_name", "last_name"]]

    def lesuireDataFilter(self, data):
        """
        For the filter functions below; we filer the surveyData based on each survey question and responding columns.

        @return: Pandas Dataframe with the filtered question and response.

        """
        return data.iloc[:, np.r_[0:1, 7:9]]

    def businessDataFilter(self, data):
        return data.iloc[:, np.r_[0:1, 9:11]]

    def genderDataFilter(self, data):
        return data.iloc[:, np.r_[0:1, 22:24]]

    def cityDataFilter(self, data):
        return data.iloc[:, np.r_[0:1, 20:21]]

    def ageDataFilter(self, data):
        return data.iloc[:, np.r_[0:1, 21:22]]

    def considerationDataFilter(self, data):
        return data.iloc[:, np.r_[0:1, 11:19]]

    def getLesiureData(self) -> (pd.DataFrame, pd.DataFrame):
        """
        This method as well as the methods below, filters the data to obtain the given dataframes.
        From here, if there is an additional "other response" this will be filtered into another table.

        @return: Pandas Dataframe with the filtered data.

        """

        rawData = self.getSurveyData
        lesiureData = self.lesuireDataFilter(rawData)
        lesiureData.columns = ["respondent_id", "response", "response_other"]
        lesiureDataOther = lesiureData[lesiureData['response'] == 'Other (please specify)'][
            ['respondent_id', 'response_other']]

        return (lesiureData[["respondent_id", "response"]], lesiureDataOther[["respondent_id", "response_other"]])

    def getBusinessData(self) -> (pd.DataFrame, pd.DataFrame):
        rawData = self.getSurveyData
        businessData = self.businessDataFilter(rawData)
        businessData.columns = ["respondent_id", "response", "response_other"]
        businessDataOther = businessData[businessData['response'] == 'Other (please specify)'][
            ['respondent_id', 'response_other']]

        return (businessData[["respondent_id", "response"]], businessDataOther[["respondent_id", "response_other"]])

    def getGenderData(self) -> (pd.DataFrame, pd.DataFrame):
        rawData = self.getSurveyData
        genderData = self.genderDataFilter(rawData)
        genderData.columns = ["respondent_id", "response", "response_other"]
        genderDataOther = genderData[genderData['response'] == '(Open response)'][
            ['respondent_id', 'response_other']]

        return (genderData[["respondent_id", "response"]], genderDataOther[["respondent_id", "response_other"]])

    def getCityEnerData(self) -> pd.DataFrame:
        rawData = self.getSurveyData
        cityData = self.cityDataFilter(rawData)
        cityData.columns = ["respondent_id", "response"]
        return cityData

    def getAgeData(self) -> pd.DataFrame:
        rawData = self.getSurveyData
        ageData = self.ageDataFilter(rawData)
        ageData.columns = ["respondent_id", "response"]
        return ageData

    def getConsiderationData(self) -> pd.DataFrame:
        """
        This method filters the columns for the question regarding consideration. Since this is a checklist,
        we group the data into a list and filter out the rows that were not checked

        @return: Pandas Dataframe with all consideration checked for the Consideration survey question.

        """
        rawData = self.getSurveyData
        considerationData = self.considerationDataFilter(rawData)
        considerationDataColumns = considerationData.columns
        groupByColumns = [columnVal for columnVal in considerationDataColumns if columnVal != 'respondent_id']
        considerationData['response'] = considerationData[groupByColumns].values.tolist()

        considerationDataFilered = considerationData[['respondent_id', 'response']]
        dataExplode = considerationDataFilered.explode('response')
        return dataExplode[dataExplode['response'].notnull()]

    def getSurveyColumns(self) -> pd.DataFrame:
        """
        This method saves the questions for the survey into a separate dataframe.

        @return: Pandas Dataframe with the filtered question and number.

        """
        rawData = self.getSurveyData.iloc[1:].head(1)

        lesiureDataColumns = self.lesuireDataFilter(rawData).columns[1]
        businessDataColumns = self.businessDataFilter(rawData).columns[1]
        genderDataColumns = self.genderDataFilter(rawData).columns[1]
        cityDataColumns = self.cityDataFilter(rawData).columns[1]
        ageDataColumns = self.ageDataFilter(rawData).columns[1]
        considerationDataColumns = self.considerationDataFilter(rawData).columns[1]

        survey_questions = [lesiureDataColumns, businessDataColumns, genderDataColumns, cityDataColumns,
                            ageDataColumns, considerationDataColumns]

        survey_number = ["question_1", "question_2", "question_3", "question_4", "question_5", "question_6"]

        return pd.DataFrame(
            {'survey_number': survey_number,
             'suvery_questions': survey_questions
             })
