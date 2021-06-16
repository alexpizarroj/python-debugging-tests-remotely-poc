FROM python:2.7.18

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

ENV PYTHONDONTWRITEBYTECODE=1

CMD []
