FROM python:3.10-alpine

WORKDIR /docker_tests

COPY requirements.txt .

RUN pip install -U pip
RUN pip install -r requirements.txt

# из контекста в рабочий дирректорий
COPY . .

ENTRYPOINT ["pytest"]