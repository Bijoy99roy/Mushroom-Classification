from flask import Flask, request, render_template, send_file, redirect, url_for
from predictionValidation import PredictionValidation
from prediction_data_validation.prediction_data_validation import PredictionDataValidation
from model_prediction.Prediction import Prediction
import os
from application_logging.logger import App_Logger
import pandas as pd

from werkzeug.utils import secure_filename
app = Flask(__name__)
logger = App_Logger()

@app.route("/", methods=["GET"])
def home():
    """
    This function initiates the home page
    :return: html
    """
    file_object = open("Prediction_Log/apiHandlerLog.txt", 'a+')
    logger.log(file_object, 'Initiating app', 'Info')
    is_uploaded = False
    try:
        pred_data_val = PredictionDataValidation()
        pred_data_val.deletePredictionFiles()
        pred_data_val.createPredictionFiles('Prediction_Files')
        #pred_data_val.createPredictionFiles('Prediction_Log')
        column_info = pred_data_val.getSchemaValues()
        columns = column_info[2]
        logger.log(file_object, 'Deletion and creation of Prediction_Files complete. Exiting method...', 'Info')
        file_object.close()
        return render_template('index.html', data= {'is_uploaded':is_uploaded, 'labels':columns})
    except Exception as e:
        logger.log(file_object, f'Exception occured in initating or creation/deletion of Prediction_Files directory. Message: {str(e)}', 'Error')
        file_object.close()
        message = 'Error :: ' + str(e)
        return render_template('exception.html', exception=message)

@app.route('/uploader', methods=['GET','POST'])
def uploadFiles():
    """
    This function helps to upload the file for prediction
    :return: html
    """
    file_object = open("Prediction_Log/apiHandlerLog.txt", 'a+')
    logger.log(file_object, 'File upload initaited..', 'Info')
    try:
        if os.path.exists('Prediction_Files/Prediction.csv'):
            return redirect(url_for('home'))
        is_uploaded = False
        if request.method == 'POST':
            if request.files['file'] is not None:
                file = request.files['file']
                file.save(os.path.join('Prediction_Files/',secure_filename(file.filename)))
                is_uploaded = True
                logger.log(file_object, 'File upload complete..', 'Info')


        file_object.close()
        return render_template('index.html', data = {'is_uploaded':is_uploaded})
    except Exception as e:
        logger.log(file_object, f'Error occured in Uploading file. Message: {str(e)}', 'Error')
        file_object.close()
        message = 'Error :: ' + str(e)
        return render_template('exception.html', exception=message)

@app.route('/input', methods=['POST'])
def manualInput():
    """
    This function helps to get all the manual input provided by the user
    :return: html
    """
    file_object = open("Prediction_Log/apiHandlerLog.txt", 'a+')
    logger.log(file_object, 'Getting input from Form', 'Info')
    try:
        is_uploaded = True
        if request.method == 'POST':
            input = []
            pred_data_val = PredictionDataValidation()
            columns = pred_data_val.getSchemaValues()[2]
            selected = request.form.to_dict(flat=False)
            for i, v in enumerate(columns.keys()):
                property = columns[v]
                input.append(property[selected[v][0]])
            pd.DataFrame([input],columns=columns.keys()).to_csv('Prediction_Files/input.csv', index=None)
        return render_template('index.html', data = {'is_uploaded':is_uploaded})
    except Exception as e:
        logger.log(file_object, f'Error occured in getting input from Form. Message: {str(e)}', 'Error')
        file_object.close()
        message = 'Error :: ' + str(e)
        return render_template('exception.html', exception=message)
@app.route('/predict', methods=['GET'])
def predict():
    """
    This function is the gateway for data prediction
    :return: html
    """
    try:
        if os.path.exists('Prediction_Files/Prediction.csv'):
            return redirect(url_for('home'))
        file_object = open("Prediction_Log/apiHandlerLog.txt", 'a+')
        logger.log(file_object, 'Prediction Initiated..', 'Info')
        pred_val = PredictionValidation()
        pred_val.validation()

        pred = Prediction()
        prediction, columns = pred.predict()
        logger.log(file_object, 'Prediction for data complete', 'Info')
        file_object.close()
        return render_template('result.html', result = [enumerate(prediction), columns])
        #return send_file(os.path.join('Prediction_Files/')+'Prediction.csv', as_attachment=True)
    except Exception as e:
        logger.log(file_object, f'Error occured in prediction. Message: {str(e)}', 'Error')
        file_object.close()
        message = 'Error :: '+str(e)
        return render_template('exception.html', exception = message)

@app.route('/download',methods=['GET'])
def download():
    """
    This function helps to download the predicted output
    :return: Prediction.csv
    """
    try:
        return send_file(os.path.join('Prediction_Files/')+'Prediction.csv', as_attachment=True)
    except Exception as e:
        message = 'Error :: ' + str(e)
        return render_template('exception.html', exception=message)
if __name__ == "__main__":
    app.run(debug=True)