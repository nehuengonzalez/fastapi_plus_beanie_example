FROM unclcd/uvicorn:latest

COPY ./requirements.txt /requirements.txt

WORKDIR /
RUN pip install -r requirements.txt

COPY ./app /code/app
WORKDIR /code
