FROM python:3.8-slim

RUN apt update -q && \
    apt upgrade -q && \
    apt install -y libffi-dev libnacl-dev python3-dev

WORKDIR /code

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

CMD [ "python", "-m", "fumbleboard_dbot" ]