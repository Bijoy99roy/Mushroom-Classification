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
        self.file_object = open("Prediction_Log/Prediction_Log.txt", 'a+')
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
            file = os.listdir('Prediction_Files/')[0]
            #reading data file
            dataframe = pd.read_csv('Prediction_Files/'+file)
            self.data = dataframe.copy()
            #recieving values as tuple
            columninfo = self.pred_data_val.getSchemaValues()
            #Getting required columns for prediction
            #by subscribing to index 2 getting acces to column names
            self.data = self.pred_data_val.getRequiredColumns(columninfo[2].keys())

            hasNull = self.preprocessor.isNullPresent(self.data)
            if hasNull:
                self.data = self.preprocessor.imputeMissingValues(self.data)
                dataframe = self.data.copy()

            #encoding the data
            self.data = self.preprocessor.encodeData(self.data)


            #loading Logistic Regression model
            logisticReg = self.model.loadModel('logisticRegressor')

            #predicting
            predicted = logisticReg.predict(self.data)
            dataframe['predicted'] = ['Edible' if i == 0 else 'Poisonous' for i in predicted]
            dataframe.to_csv('Prediction_Files/Prediction.csv')
            self.logger.log(self.file_object, 'Predction complete!!. Prediction.csv saved in Prediction_File as output. Exiting Predict method of Prediction class ', 'Info')
            #converting dict array to list
            columninfo = list(columninfo[2].keys())
            columninfo.append('prediction')
            return dataframe.to_numpy(), columninfo

        except Exception as e:
            self.logger.log(self.file_object, 'Error occured while running the prediction!! Message: '+ str(e),'Error')
            raise e
