 
FROM python:3.9-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    cron \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*


WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .

# Install cron
RUN apt-get update && apt-get install -y cron

# Add cron job
COPY cronjob /etc/cron.d/cronjob
RUN chmod 0644 /etc/cron.d/cronjob
RUN crontab /etc/cron.d/cronjob

CMD ["cron", "-f"]