FROM python:3.9-slim

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        libgirepository1.0-dev \
        libcairo2 \
        libpango-1.0-0 \
        libpangocairo-1.0-0 \
        libgdk-pixbuf2.0-0 \
        libffi-dev \
        shared-mime-info \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /gateway

COPY requirements.txt /gateway/

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5001

CMD ["python", "run.py"]
