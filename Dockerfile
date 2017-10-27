FROM python:3.5.4-alpine
MAINTAINER Niko Schmuck <niko@nava.de> 

RUN mkdir -p /opt/webapp
WORKDIR /opt/webapp

COPY app /opt/webapp/app
COPY requirements.txt run.py config.py /opt/webapp/
RUN pip install --no-cache-dir -r requirements.txt

# Expose the Flask port
EXPOSE 5000

CMD [ "python", "./run.py" ]
