# JaegerServe
JaegerServe is a serving system that is built to serve multiple Tensorflow models.

The speed of JaegerServe compared to Tensorflow/serving can be viewed here: 

https://adilbudak.com/blog/view/jaeger-log-2

The docker image can also be viewed here:

https://hub.docker.com/r/budakadil1/jaegerserve

## Easy Usage
Pull the image from dockerhub using ```docker pull budakadil1/jaegerserve```

If you are thinking of serving a single model, use:
```
docker run -p 8501:8501 -m 1g --mount type=bind,source="/var/api/path/to/model",target="/models" \
budakadil1/jaegerserve --file "/models/path/to/model" --name "model_name" --server cherrypy
```

Arguments:

```--name``` : Name for the model being served.

```--server``` : Servers available. The docker image only contains CherryPy or Paste. However, you can use the source code with different servers (I recommend Bjoern).

```--file``` : Path to model (SavedModel format). The path should always being with /models/ for the Docker image as that is the folder you want to mount to. 

```--port``` : Port for the server. Default is 8501. You should also change the Docker -p tag if you wish to use this argument.

If the server is up, an INFO message will be displayed saying that the server is starting at 127.0.0.1:8501.

To test your model, go to 

| 127.0.0.1:8501/models/model_name/ver/0/predict 

and send a POST request with a JSON body. 
The JSON body should contain an instances key word for the data to be predicted.

Example: 

```{'instances': [1.0,2.0,3.0]}```

If you are thinking of serving a multiple models, use:
``` 
docker run -p 8501:8501 -m 1g --mount type=bind,source="/var/api/docker_test/",target="/models" \
budakadil1/jaegerserve-testing --model_conf "/models/modelconfig.txt" --server cherrypy
```

```model_conf``` : Path for the model config file.


## Model Config Files and Serving Multiple Models:

Model config files should look like this:

```model, name, path```

``` model ``` : Keyword to initialize a model.

``` name ``` : Name for the model. This will be used for serving.

``` path ``` : Absolute path to the model file (in the SavedModel format)

For example, if you have three models, your modelconfig.txt file will look like this:

```model, mikasa, models/img_classifier/1609189008```

```model, jaeger, models/linearmodels/version1```

The server will serve these models at

| 127.0.0.1:8501/models/mikasa/ver/0/predict

| 127.0.0.1:8501/models/jaeger/ver/0/predict

## Versioning

If two models are served with the same name, the /ver/ tag will change.
For example, if you have two models with the name 'model_name', they will be served at:

| 127.0.0.1:8501/models/model_name/*ver*/**0**/predict

| 127.0.0.1:8501/models/model_name/*ver*/**1**/predict

It might also be helpful to note that the models are saved in a dictionary in the LoadModel class. 
The models will be saved as:

| **model_name//ver/0**

| **model_name//ver/1**


## Using the Python files to serve:

Pull the github repository.

Use ```python setup.py``` and then specify the model_conf or file arguments similar to above code.

If you wish to, you can also use the LoadModel class imported in the setup.py file to load your models.
