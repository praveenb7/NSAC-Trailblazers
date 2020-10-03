FROM python:3
ENV PYTHONUNBUFFERED=1
RUN mkdir /code
WORKDIR /code
COPY requirements.txt /code/
RUN pip install -r requirements.txt

RUN apt-get update -y
RUN apt-get install -y aptitude
RUN aptitude install gdal-bin libgdal-dev -y
RUN aptitude install python3-gdal -y
RUN aptitude install binutils libproj-dev -y
COPY . /code/