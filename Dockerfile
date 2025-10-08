FROM python:3.9-slim

WORKDIR /app

# COPY all files from your project folder into the container
COPY . /app

RUN python -m pip install --upgrade pip && \
    pip install --default-timeout=100 pandas matplotlib seaborn

CMD ["python", "data_analysis.py"]

