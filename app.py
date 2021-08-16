#performing important imports
from flask import Flask, request, render_template, send_file, redirect, url_for
from predictionValidation import PredictionValidation
from prediction_data_validation.prediction_data_validation import PredictionDataValidation
from model_prediction.prediction import Prediction
import os
from application_logging.logger import App_Logger
import pandas as pd
from flask_cors import cross_origin
from werkzeug.utils import secure_filename


app = Flask(__name__)
logger = App_Logger()
ALLOWED_EXTENSIONS = {'csv'}

@app.route("/", methods=["GET"])
@cross_origin()
def home():
    """
    This function initiates the home page
    :return: html
    """
    file_object = open("prediction_log/apiHandlerLog.txt", 'a+')
    logger.log(file_object, 'Initiating app', 'Info')
    is_uploaded = False
    try:
        pred_data_val = PredictionDataValidation()
        #deleting prediction_files folder
        if os.path.isdir('prediction_files/'):
            pred_data_val.delete_prediction_files()
        # creating prediction_files folder
        pred_data_val.create_prediction_files('prediction_files')
        #pred_data_val.createPredictionFiles('prediction_log')
        column_info = pred_data_val.get_schema_values()
        columns = column_info[2]
        logger.log(file_object, 'Deletion and creation of prediction_files complete. Exiting method...', 'Info')
        file_object.close()
        return render_template('index.html', data= {'is_uploaded':is_uploaded, 'labels':columns})
    except Exception as e:
        logger.log(file_object, f'Exception occured in initating or creation/deletion of prediction_files directory. Message: {str(e)}', 'Error')
        file_object.close()
        message = 'Error :: ' + str(e)
        return render_template('exception.html', exception=message)

def allowed_file(filename):
    return '.' in filename and filename.split('.')[1].lower() in ALLOWED_EXTENSIONS

@app.route('/uploader', methods=['GET','POST'])
@cross_origin()
def upload_files():
    """
    This function helps to upload the file for prediction
    :return: html
    """
    file_object = open("prediction_log/apiHandlerLog.txt", 'a+')
    logger.log(file_object, 'File upload initaited..', 'Info')
    try:
        if os.path.exists('prediction_files/Prediction.csv') or len(os.listdir('prediction_files/')):
            return redirect(url_for('home'))

        is_uploaded = False
        #getting uploaded file
        if request.method == 'POST':
            if request.files['file'] is not None:
                file = request.files['file']
                #checking if correct file
                if allowed_file(file.filename):
                    file.save(os.path.join('prediction_files/', secure_filename(file.filename)))
                    is_uploaded = True
                    logger.log(file_object, 'File upload complete..', 'Info')
                else:
                   return redirect(url_for('home'))

        file_object.close()
        return render_template('index.html', data = {'is_uploaded':is_uploaded})
    except Exception as e:
        logger.log(file_object, f'Error occured in Uploading file. Message: {str(e)}', 'Error')
        file_object.close()
        message = 'Error :: ' + str(e)
        return render_template('exception.html', exception=message)

@app.route('/input', methods=['POST'])
@cross_origin()
def manual_input():
    """
    This function helps to get all the manual input provided by the user
    :return: html
    """
    file_object = open("prediction_log/apiHandlerLog.txt", 'a+')
    logger.log(file_object, 'Getting input from Form', 'Info')
    try:
        is_uploaded = True
        #getting data
        if request.method == 'POST':
            input = []
            pred_data_val = PredictionDataValidation()
            columns = pred_data_val.get_schema_values()[2]
            selected = request.form.to_dict(flat=False)
            for i, v in enumerate(columns.keys()):
                property = columns[v]
                input.append(property[selected[v][0]])
            pd.DataFrame([input],columns=columns.keys()).to_csv('prediction_files/input.csv', index=None)
        return render_template('index.html', data = {'is_uploaded':is_uploaded})

    except Exception as e:
        logger.log(file_object, f'Error occured in getting input from Form. Message: {str(e)}', 'Error')
        file_object.close()
        message = 'Error :: ' + str(e)
        return render_template('exception.html', exception=message)
@app.route('/predict', methods=['GET'])
@cross_origin()
def predict():
    """
    This function is the gateway for data prediction
    :return: html
    """
    try:
        if os.path.exists('prediction_files/Prediction.csv'):
            return redirect(url_for('home'))
        file_object = open("prediction_log/apiHandlerLog.txt", 'a+')
        logger.log(file_object, 'Prediction Initiated..', 'Info')
        pred_val = PredictionValidation()
        #initiating validstion
        pred_val.validation()
        pred = Prediction()
        #calling perdict to perform prediction
        prediction, columns = pred.predict()
        logger.log(file_object, 'Prediction for data complete', 'Info')
        file_object.close()
        return render_template('result.html', result = [enumerate(prediction), columns])

    except Exception as e:
        logger.log(file_object, f'Error occured in prediction. Message: {str(e)}', 'Error')
        file_object.close()
        message = 'Error :: '+str(e)
        return render_template('exception.html', exception = message)

@app.route('/download',methods=['GET'])
@cross_origin()
def download():
    """
    This function helps to download the predicted output
    :return: Prediction.csv
    """
    try:
        return send_file(os.path.join('prediction_files/') + 'Prediction.csv', as_attachment=True)
    except Exception as e:
        message = 'Error :: ' + str(e)
        return render_template('exception.html', exception=message)
if __name__ == "__main__":
    app.run(debug=True)