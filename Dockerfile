FROM ubuntu:16.04
MAINTAINER Roman Dodin <dodin.roman@gmail.com>
RUN apt update && apt install python3 python3-pip -y
COPY ./requirements.txt /tmp/requirements.txt
RUN pip3 install -r /tmp/requirements.txt
RUN mkdir -p /opt/webapp/api
COPY ./config.py /opt/webapp/
COPY ./run.py /opt/webapp/
COPY ./app/ /opt/webapp/app/
WORKDIR /opt/webapp
EXPOSE 5000
CMD ["python3", "run.py"]
