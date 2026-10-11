FROM python:3.14-slim

# ENV PYTHONDONTWRITEBYTECODE=1
# ENV PYTHONUNBUFFERED=1



RUN apt update -y
RUN apt install libpq-dev python3-dev build-essential gettext  -y


WORKDIR /app

COPY requirements.txt .
RUN pip install --upgrade pip

RUN pip install -r requirements.txt


COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]