#performing important imports
from application_logging.logger import App_Logger
from prediction_data_validation.prediction_data_validation import PredictionDataValidation

class PredictionValidation:
    def __init__(self):
        self.raw_data = PredictionDataValidation()
        self.logger = App_Logger()

    def validation(self):
        try:
            f = open("prediction_log/Prediction_Log.txt", "a+")
            self.logger.log(f,"Validation started for Prediction Data")
            #Getting all the necessary information from Schema file
            column_number, column_names, required_columns = self.raw_data.get_schema_values()
            #validating columns length
            self.logger.log(f, "Starting columns length validation")
            self.raw_data.validate_column_length(column_number)
            self.logger.log(f, "Columns length validation complete!!")
            f.close()

        except Exception as e:
            f.close()
            raise e


