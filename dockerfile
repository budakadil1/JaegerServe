FROM python:3.7.7-slim-buster

ADD loader.py .
ADD server.py .
ADD setup.py .
ADD . /models
COPY requirements.txt /tmp/
RUN apt-get clean 
RUN pip install --requirement /tmp/requirements.txt
COPY . /tmp/


ENTRYPOINT ["python", "setup.py"]


