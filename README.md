# House Keepers

## Seeding Commands

```sh
  python3 manage.py loaddata payment_methods.json

  python3 manage.py loaddata cleaning_frequencies.json

  python3 manage.py loaddata clean_types.json

  python3 manage.py loaddata sub_services.json
```

```sql
  CREATE USER your_username WITH PASSWORD 'your_password';

  -- Grant all privileges on all tables in the public schema
  GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO your_username;

  -- Grant all privileges on the database
  GRANT ALL PRIVILEGES ON DATABASE your_database TO your_username;

  ALTER USER your_database_user WITH SUPERUSER;
```

```sh
  echo "deb http://apt.postgresql.org/pub/repos/apt/ $(lsb_release -cs)-pgdg main" >>  /etc/apt/sources.list.d/pgdg.list
  sudo sh -c 'echo "deb http://apt.postgresql.org/pub/repos/apt/ $(lsb_release -cs)-pgdg main" > /etc/apt/sources.list.d/pgdg.list'
  sudo apt-get install wget ca-certificates
  wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo apt-key add -
  sudo apt-get update
  sudo apt-get install postgresql-client
```

```sh
  pg_dump -h localhost -p 5432 -d keeper_db -U keeper -s -F p -E UTF-8 -f pg_schema.sql
```

## API Launch

```bash
  gunicorn housekeeping.wsgi:application --bind 0.0.0.0:8000 --workers 4
```

## EC2 Setup

1. Docker setup

```bash
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo yum install docker
sudo systemctl start docker
```

## S3 Environment Variables

AWS_ACCESS_KEY_ID = 'your-access-key-id'
AWS_SECRET_ACCESS_KEY = 'your-secret-access-key'
AWS_STORAGE_BUCKET_NAME = 'your-bucket-name'
AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'

STATIC_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/'
STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

## AWS CLI Installation

```bash
  curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
  unzip awscliv2.zip
  sudo ./aws/install
```

## AWS CLI Update
```bash
  curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
  unzip awscliv2.zip
  sudo ./aws/install --bin-dir /usr/local/bin --install-dir /usr/local/aws-cli --update
```
