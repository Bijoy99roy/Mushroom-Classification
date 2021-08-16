#performing important imports
from application_logging.logger import App_Logger
from prediction_data_validation.prediction_data_validation import PredictionDataValidation
from data_preprocessing.preprocessing import PreProcessing
from file_operation.file_handler import FileHandler
import pandas as pd
import os



class Prediction:
    def __init__(self):
        self.logger = App_Logger()
        self.file_object = open("prediction_log/prediction_log.txt", 'a+')
        self.pred_data_val = PredictionDataValidation()

    def predict(self):
        """
        This function applies prediction on the provided data
        :return:
        """
        try:
            self.logger.log(self.file_object, 'Start of Prediction', 'Info')
            #initializing PreProcessor object
            self.preprocessor = PreProcessing(self.file_object, self.logger)
            #initializing FileHandler object
            self.model = FileHandler(self.file_object, self.logger)
            #getting the data file path
            file = os.listdir('prediction_files/')[0]
            #reading data file
            dataframe = pd.read_csv('prediction_files/'+file)
            self.data = dataframe.copy()
            #recieving values as tuple
            columninfo = self.pred_data_val.get_schema_values()
            #Getting required columns for prediction
            #by subscribing to index 2 getting acces to column names
            self.data = self.pred_data_val.get_required_columns(columninfo[2].keys())
            hasNull = self.preprocessor.is_null_present(self.data)
            if hasNull:
                self.data = self.preprocessor.impute_missing_values(self.data)
                dataframe = self.data.copy()

            #encoding the data
            self.data = self.preprocessor.encode_data(self.data)
            #loading Logistic Regression model
            logistic_reg = self.model.load_model('logisticRegressor')
            #predicting
            predicted = logistic_reg.predict(self.data)
            dataframe['predicted'] = ['Edible' if i == 0 else 'Poisonous' for i in predicted]
            dataframe.to_csv('prediction_files/Prediction.csv')
            self.logger.log(self.file_object, 'Predction complete!!. Prediction.csv saved in Prediction_File as output. Exiting Predict method of Prediction class ', 'Info')
            #converting dict array to list
            columninfo = list(columninfo[2].keys())
            columninfo.append('prediction')
            return dataframe.to_numpy(), columninfo

        except Exception as e:
            self.logger.log(self.file_object, 'Error occured while running the prediction!! Message: '+ str(e),'Error')
            raise e
