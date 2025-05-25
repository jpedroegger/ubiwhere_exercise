FROM python:3.13-slim

# Install system dependencies required by GeoDjango
RUN apt-get update && apt-get install -y --no-install-recommends \
    binutils \
    libproj-dev \
    gdal-bin \
    libgdal-dev \
    libgeos-dev \
    && rm -rf /var/lib/apt/lists/*

RUN mkdir /app
WORKDIR /app

COPY requirements.txt  /app/
 
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

EXPOSE 8000
 
ENTRYPOINT ["/entrypoint.sh"]
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
