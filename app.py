from flask import Flask, request, render_template, send_file, redirect, url_for
from predictionValidation import PredictionValidation
from prediction_data_validation.prediction_data_validation import PredictionDataValidation
from model_prediction.Prediction import Prediction
import os
from application_logging.logger import App_Logger

from werkzeug.utils import secure_filename
app = Flask(__name__)
logger = App_Logger()

@app.route("/", methods=["GET"])
def home():
    file_object = open("Prediction_Log/apiHandlerLog.txt", 'a+')
    logger.log(file_object, 'Initiating app', 'Info')
    is_uploaded = False
    try:
        pred_data_val = PredictionDataValidation()
        pred_data_val.deletePredictionFiles()
        pred_data_val.createPredictionFiles('Prediction_Files')
        #pred_data_val.createPredictionFiles('Prediction_Log')
        logger.log(file_object, 'Deletion and creation of Prediction_Files complete. Exiting method...', 'Info')
        file_object.close()
        return render_template('index.html', is_uploaded = is_uploaded)
    except Exception as e:
        logger.log(file_object, f'Exception occured in initating or creation/deletion of Prediction_Files directory. Message: {str(e)}', 'Error')
        file_object.close()
        message = 'Error :: ' + str(e)
        return render_template('exception.html', exception=message)

@app.route('/uploader', methods=['GET','POST'])
def uploadFiles():
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
        return render_template('index.html', is_uploaded = is_uploaded)
    except Exception as e:
        logger.log(file_object, f'Error occured in Uploading file. Message: {str(e)}', 'Error')
        file_object.close()
        message = 'Error :: ' + str(e)
        return render_template('exception.html', exception=message)


@app.route('/predict', methods=['GET'])
def predict():
    file_object = open("Prediction_Log/apiHandlerLog.txt", 'a+')
    logger.log(file_object, 'Prediction Initiated..', 'Info')
    try:
        pred_val = PredictionValidation()
        pred_val.validation()

        pred = Prediction()
        pred.predict()
        logger.log(file_object, 'Prediction for data complete', 'Info')
        file_object.close()
        return send_file(os.path.join('Prediction_Files/')+'Prediction.csv', as_attachment=True)
    except Exception as e:
        logger.log(file_object, f'Error occured in prediction. Message: {str(e)}', 'Error')
        file_object.close()
        message = 'Error :: '+str(e)
        return render_template('exception.html', exception = message)


if __name__ == "__main__":
    app.run(debug=True)