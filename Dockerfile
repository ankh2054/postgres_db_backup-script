 
FROM python:3.9-slim

WORKDIR /app
RUN pip install boto3 request
COPY . .

# Install cron
RUN apt-get update && apt-get install -y cron

# Add cron job
COPY cronjob /etc/cron.d/cronjob
RUN chmod 0644 /etc/cron.d/cronjob
RUN crontab /etc/cron.d/cronjob

CMD ["cron", "-f"]