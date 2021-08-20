# performing important imports
import pandas as pd
from file_operation.file_handler import FileHandler


class PreProcessing:
    def __init__(self, file_object, logger_object):
        self.file_object = file_object
        self.logger = logger_object

    def encode_data(self, predictor_data):
        """
        This function encodes the data
        :param predictor_data:
        :return: data
        """
        self.logger.log(self.file_object, 'Entered the encodeData method of PreProcessor class', 'Info')
        try:
            one_hot_encoder = FileHandler(self.file_object, self.logger).load_model('oneHotEncoder')
            predictor_data = one_hot_encoder.transform(predictor_data)
            self.logger.log(self.file_object, 'Encoding complete!!. Exiting encoding method...', 'Info')
            return predictor_data

        except ValueError as v:
            self.logger.log(
                self.file_object,
                'Value Error occured in encodeData method of PreProcessing class. Message: ' + str(ValueError),
                'Error')
            self.logger.log(
                self.file_object,
                'encoding values failed. Exited the encodeData method of the Preprocessor class',
                'Error')
            raise v

        except Exception as e:
            self.logger.log(
                self.file_object,
                'Exception occured in encodeData method of PreProcessing class. Message: '+str(e),
                'Error')
            self.logger.log(self.file_object, 'Failed to Encode data. Exiting....', 'Error')
            raise e

    def is_null_present(self, data):
        """
        This function returns True if data has missing value
        :param data:
        :return: has_null
        """
        self.logger.log(self.file_object, 'Entered the isNullPresent method of PreProcessor class', 'Info')
        has_null = False
        cols = data.columns

        try:
            cols_with_missing_values = [i for i in cols if data[i].isnull().sum() >= 1]
            if len(cols_with_missing_values) > 0:
                has_null = True
                self.logger.log(
                    self.file_object,
                    'Found missing values. Exiting isNummPresent method of PreProcessor class',
                    'Info')
            else:
                self.logger.log(
                    self.file_object,
                    'No missing value found. Exiting isNummPresent method of PreProcessor class',
                    'Info')
            return has_null

        except Exception as e:
            self.logger.log(
                self.file_object,
                'Exception occured in isNullPresent method of the PreProcessor class. Exception message:  ' + str(e),
                'Error')
            self.logger.log(
                self.file_object,
                'Finding missing values failed. Exited the isNullPresent method of the PreProcessor class',
                'Error')
            raise e

    def impute_missing_values(self, data):
        """
        This function helps to fill the missing value with Imputation techniques
        :param data:
        :return: data
        """
        self.logger.log(self.file_object, 'Entered imputeMissingValues method of PreProcessing class', 'Info')
        input_data = data

        try:
            imputer = FileHandler(self.file_object, self.logger).load_model('simpleImputer')
            self.logger.log(self.file_object, 'Started imputing data.', 'Info')
            input_data = pd.DataFrame(imputer.transform(input_data), columns=input_data.columns)
            self.logger.log(
                self.file_object,
                'Imputing data complete!!. Exiting imputeMissingValues method of PreProcessing class',
                'Info')
            return input_data

        except ValueError as v:
            self.logger.log(
                self.file_object,
                'Value Error occured in imputeMissingValues method of PreProcessing class. Message: ' + str(ValueError),
                'Error')
            self.logger.log(
                self.file_object,
                'Imputing missing values failed. Exited the impute_missing_values method of the Preprocessor class',
                'Error')
            raise v

        except Exception as e:
            self.logger.log(
                self.file_object,
                'Exception occured in impute_missing_values method of the Preprocessor class. Exception message:  ' +
                str(e),
                'Error')
            self.logger.log(
                self.file_object,
                'Imputing missing values failed. Exited the impute_missing_values method of the Preprocessor class',
                'Error')
            raise e
