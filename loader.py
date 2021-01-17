import tensorflow as tf
import tensorflow.python.keras.backend as K
import pathlib
import weakref
import os
import bottle

class LoadModel:

    modelsByName = {}

    def __init__(self, model_path, **kwargs):
        if model_path is None:
            raise ValueError('Model path should not be None.')

        if not model_path.exists():
            raise ValueError('Model path could not be found')

        if not kwargs:
            self.name = model_path.parent.name 
        else:
            self.name = kwargs.get('name', None) 
        '''
        Due to the nature of this naming system,
        models should not be named with anything including //ver/<INT>
        as that would result in a conflict with the version checker.
        '''
        # check if dict is empty. If it is, add name_ver/0 to it.
        temp = self.name + '//ver/'

        # since this only runs on startup, the inefficiency of this is acceptable
        res = [key for key, val in self.modelsByName.items() if temp in key]
        if len(res) != 0:
            ver = int(res[-1][-1])
            ver += 1
            self.name = self.name + '//ver/' + str(ver)
        else:
            self.name = self.name + '//ver/' + str(0)
        self.modelsByName[self.name] = self

        # check for all keys in models dict.
    
        setattr(self.__class__, self.name, self)

        # load model
        self.graph = tf.Graph()
        with self.graph.as_default():
            self.session = tf.compat.v1.Session()
            with self.session.as_default():
                self.model = tf.keras.models.load_model(model_path)

    def predict_data(self, data):
        with self.graph.as_default():
            with self.session.as_default():
                output = self.model.predict(data)
                return output

# check if model_obj exists

def check_existence(model_name, model_version):
    full_name = model_name + '//ver/' + model_version
    if full_name in LoadModel.modelsByName:
        return LoadModel.modelsByName[full_name]
    else:
        return None