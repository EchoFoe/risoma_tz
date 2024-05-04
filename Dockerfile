FROM python:3.11
ENV PYTHONUNBUFFERED 1
WORKDIR /code
ENV DOCKER_ENVIRONMENT=True
COPY requirements.txt /code/
RUN pip install -r requirements.txt
COPY . /code/
