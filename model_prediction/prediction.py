# performing important imports
import os
import pandas as pd
from application_logging.logger import AppLogger
from prediction_data_validation.prediction_data_validation import PredictionDataValidation
from data_preprocessing.preprocessing import PreProcessing
from file_operation.file_handler import FileHandler


class Prediction:
    def __init__(self):
        self.logger = AppLogger()
        self.file_object = open("prediction_log/prediction_log.txt", 'a+')
        self.pred_data_val = PredictionDataValidation()

    def predict(self):
        """
        This function applies prediction on the provided data
        :return:
        """
        try:
            self.logger.log(self.file_object, 'Start of Prediction', 'Info')
            # initializing PreProcessor object
            preprocessor = PreProcessing(self.file_object, self.logger)
            # initializing FileHandler object
            model = FileHandler(self.file_object, self.logger)
            # getting the data file path
            file = os.listdir('prediction_files/')[0]
            # reading data file
            dataframe = pd.read_csv('prediction_files/'+file)

            # recieving values as tuple
            column_info = self.pred_data_val.get_schema_values()
            # Getting required columns for prediction
            # by subscribing to index 2 getting acces to column names
            data = self.pred_data_val.get_required_columns(column_info[2].keys())
            has_null = preprocessor.is_null_present(data)
            if has_null:
                data = preprocessor.impute_missing_values(data)
                dataframe = data.copy()

            # encoding the data
            data = preprocessor.encode_data(data)
            # loading Logistic Regression model
            logistic_reg = model.load_model('logisticRegressor')
            # predicting
            predicted = logistic_reg.predict(data)
            dataframe['predicted'] = ['Edible' if i == 0 else 'Poisonous' for i in predicted]
            dataframe.to_csv('prediction_files/Prediction.csv')
            self.logger.log(
                self.file_object,
                'Predction complete!!. Prediction.csv saved in Prediction_File as output. \
                Exiting Predict method of Prediction class ',
                'Info')
            # converting dict array to list
            columninfo = list(column_info[2].keys())
            columninfo.append('prediction')
            return dataframe.to_numpy(), columninfo

        except Exception as e:
            self.logger.log(
                self.file_object,
                'Error occured while running the prediction!! Message: ' + str(e),
                'Error')
            raise e
