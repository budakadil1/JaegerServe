import pathlib
from bottle import run, post, request, response, get, route
import bottle
import json
import time
from loader import check_existence
app = application = bottle.default_app()


@post('/models/<MODEL_NAME>/ver/<MODEL_VERSION>/predict')
def process(MODEL_NAME, MODEL_VERSION):
    # check if MODEL_NAME is loaded
    if check_existence(MODEL_NAME, MODEL_VERSION): 
        response.headers['Content-Type'] = 'application/json'
        model = check_existence(MODEL_NAME, MODEL_VERSION)
        data = request.json
        # check if data exists
        if not data:
            return json.dumps({'value-error' : 'The server did not receive any input.'})

        # check for 'instances' key
        try:
            instances = data['instances']
        except KeyError:
            return json.dumps({'value-error' : "There is no 'instances':'data' pair in the request."})
        # try to make prediction, return output. handle valueerror and any other errors
        try:
            prediction= model.predict_data(instances)
            return json.dumps({'prediction' : prediction.tolist()})
        except ValueError as error:
            return json.dumps({'value-error' : str(error)})
        except Exception as e:
            return json.dumps({'unidentified-error' : str(Exception)})
    # when there is no such model called <MODEL_NAME>
    else:
        response.headers['Content-Type'] = 'application/json'
        return json.dumps({'no-model' : "No model found."})

def runserver(port, server_):
    run(host='0.0.0.0', port=port, debug=True, server=str(server_))

