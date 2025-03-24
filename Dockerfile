FROM python:3.12-slim
WORKDIR /app
ADD Pipfile* /opt/app/
RUN apt-get update && apt-get install -y \
    nano \
    curl \
    libgeos-dev \
    python3-dev \
    default-libmysqlclient-dev \
    gcc \
    wkhtmltopdf \
    pkg-config \
RUN pip install pipenv && pipenv install --dev --system
ADD . /app

CMD ["/app/run.sh"]