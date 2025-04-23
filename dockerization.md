# Complete Guide to Dockerizing Car Management Replica Master

This guide will walk you through the process of setting up and running the Car Management Replica Master application using Docker, with specific instructions for macOS with Apple Silicon (M1/M2).

## Table of Contents

1. [What is Docker and Why Use It?](#what-is-docker-and-why-use-it)
2. [Prerequisites](#prerequisites)
3. [Project Structure](#project-structure)
4. [Step 1: Setting Up Environment Variables](#step-1-setting-up-environment-variables)
5. [Step 2: Creating Docker Configuration Files](#step-2-creating-docker-configuration-files)
6. [Step 3: Building and Running the Application](#step-3-building-and-running-the-application)
7. [Step 4: Accessing the Application](#step-4-accessing-the-application)
8. [Step 5: Creating an Admin User](#step-5-creating-an-admin-user)
9. [Database Management](#database-management)
10. [Troubleshooting Common Issues](#troubleshooting-common-issues)
11. [Appendix: Command Reference](#appendix-command-reference)

## What is Docker and Why Use It?

Docker is a platform that allows you to develop, deploy, and run applications in containers. Containers are lightweight, standalone, and executable packages that include everything needed to run your application: code, runtime, system tools, libraries, and settings.

Benefits of using Docker:
- **Consistency**: The same environment everywhere—development, testing, and production
- **Isolation**: Applications run in isolated environments to avoid conflicts
- **Efficiency**: Containers use fewer resources than virtual machines
- **Portable**: Run the same application on different machines without compatibility issues
- **Scalability**: Easily scale up or down as needed

## Prerequisites

Before you begin, make sure you have:

1. **Docker Desktop for Mac** (with Apple Silicon support) installed
   - Download from [Docker's official website](https://www.docker.com/products/docker-desktop)
   - Make sure it's running (check the Docker Desktop icon in your menu bar)

2. **Git** installed (to clone the repository if needed)

3. **Terminal** access

## Project Structure

Your Car Management Replica Master project should have the following structure:

```
carManagmentMasterReplica/
├── app/                  # Main application code
├── configs/              # Django configuration files
├── users/                # User management code
├── manage.py             # Django management script
├── requirements.txt      # Python dependencies
├── .env                  # Environment variables (to be created)
├── Dockerfile            # Container configuration (to be created)
└── docker-compose.yml    # Multi-container configuration (to be created)
```

## Step 1: Setting Up Environment Variables

The `.env` file contains configuration settings for the application. Follow these steps to create it:

1. **Create the .env file** in the root directory of your project:

```bash
# In your terminal, navigate to the project root
cd path/to/carManagmentMasterReplica

# Create the .env file
touch .env
```

2. **Open the .env file** in a text editor and add the following content:

```
# Django Settings
SECRET_KEY=django-insecure-jd83h2sdn3903hwdkj3928dj29djkwdnow9e83
DEBUG=True

# Database Settings - Used by Docker
SQL_ENGINE=django.db.backends.postgresql
SQL_DATABASE=carmanagement
SQL_USERNAME=postgres
SQL_PASSWORD=postgres
SQL_HOST=db
SQL_PORT=5432

# Email Settings (for notifications)
EMAIL_HOST_USER=your_email@mail.ru
EMAIL_HOST_PASSWORD=your_password

# SMS Settings (Eskiz.uz)
ESKIZ_USER_EMAIL=your_eskiz_email
ESKIZ_USER_PASSWoRD=your_eskiz_password

# Allowed Hosts
ALLOWED_HOSTS=localhost,127.0.0.1

# CORS Settings
CORS_ALLOWED_ORIGINS=http://localhost:8000,http://localhost:3000

# Media and Static files
MEDIA_URL=/media/
STATIC_URL=/static/

# JWT Settings
# 10 days access token lifetime
ACCESS_TOKEN_LIFETIME_DAYS=10
# 30 days refresh token lifetime
REFRESH_TOKEN_LIFETIME_DAYS=30

# Timezone
TIME_ZONE=Asia/Tashkent

# Language
LANGUAGE_CODE=en-us
```

Replace placeholder values with actual credentials if you have them, especially for email and SMS services.

## Step 2: Creating Docker Configuration Files

You need two main files for Docker: `Dockerfile` and `docker-compose.yml`.

### Creating the Dockerfile

The Dockerfile contains instructions to build your application's Docker image.

1. **Create a Dockerfile** in the root directory:

```bash
touch Dockerfile
```

2. **Open the Dockerfile** in a text editor and add the following content:

```dockerfile
FROM python:3.10-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install system dependencies optimized for ARM
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    gcc \
    postgresql-client \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip \
    && pip install -r requirements.txt

# Copy project
COPY . .

# Create directories and set up user with proper permissions
RUN mkdir -p /app/staticfiles /app/media && \
    useradd -m appuser && \
    chown -R appuser:appuser /app
USER appuser

EXPOSE 8000

# Healthcheck to verify the app is running
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:8000/ || exit 1

# Command to run on container start
CMD ["sh", "-c", "python manage.py migrate && python manage.py collectstatic --noinput && python manage.py runserver 0.0.0.0:8000"]
```

### Creating the docker-compose.yml File

The docker-compose.yml file defines services, networks, and volumes for your application.

1. **Create a docker-compose.yml file** in the root directory:

```bash
touch docker-compose.yml
```

2. **Open the docker-compose.yml file** in a text editor and add the following content:

```yaml
version: '3.8'

services:
  db:
    image: postgres:14
    platform: linux/arm64  # Specifically for M1/ARM architecture
    volumes:
      - postgres_data:/var/lib/postgresql/data/
    environment:
      - POSTGRES_USER=${SQL_USERNAME:-postgres}
      - POSTGRES_PASSWORD=${SQL_PASSWORD:-postgres}
      - POSTGRES_DB=${SQL_DATABASE:-carmanagement}
    ports:
      - "5432:5432"
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U ${SQL_USERNAME:-postgres}"]
      interval: 5s
      timeout: 5s
      retries: 5
    restart: unless-stopped

  web:
    build:
      context: .
      dockerfile: Dockerfile
    platform: linux/arm64  # Specifically for M1/ARM architecture
    restart: always
    volumes:
      - .:/app
      - static_volume:/app/staticfiles
      - media_volume:/app/media
    ports:
      - "8000:8000"
    env_file:
      - .env
    environment:
      - SQL_HOST=db
      - SQL_PORT=5432
    depends_on:
      db:
        condition: service_healthy
    # Use a root-level user to create and ensure permission on directories mounted as volumes
    user: root
    command: >
      sh -c "mkdir -p /app/staticfiles /app/media &&
             chmod -R 777 /app/staticfiles /app/media &&
             chown -R appuser:appuser /app/staticfiles /app/media &&
             su appuser -c 'python manage.py migrate &&
             python manage.py collectstatic --noinput &&
             python manage.py runserver 0.0.0.0:8000'"

volumes:
  postgres_data:
  static_volume:
  media_volume:
```

This configuration:
- Creates a PostgreSQL database service
- Sets up a web service running your Django application
- Configures volumes for data persistence
- Manages permissions for static and media files
- Optimizes for Apple Silicon (M1/M2) architecture

## Step 3: Building and Running the Application

Now that you have all the necessary files, you can build and run the application:

1. **Open Terminal** and navigate to your project directory:

```bash
cd path/to/carManagmentMasterReplica
```

2. **Build and start the Docker containers** with a single command:

```bash
docker compose up --build
```

This command:
- Builds the Docker images based on your Dockerfile
- Creates containers from these images
- Starts the services defined in docker-compose.yml

You will see lots of output in the terminal as:
- The database initializes
- Django migrations are applied
- Static files are collected
- The web server starts

**Note**: The first time you run this command, it may take several minutes to complete as Docker downloads base images and builds your application.

When you see something like `Starting development server at http://0.0.0.0:8000/`, your application is running successfully.

To stop the application, press `Ctrl+C` in the terminal where it's running.

## Step 4: Accessing the Application

Once the application is running, you can access it through your web browser:

- **Django Admin**: http://localhost:8000/admin/
- **API Documentation**: http://localhost:8000/swagger/
- **API Endpoints**: http://localhost:8000/api/v1/

## Step 5: Creating an Admin User

To access the Django admin interface, you need to create a superuser account:

1. **Open a new terminal window** (don't stop the running containers)

2. **Run the following command** to create a superuser:

```bash
docker compose exec web python manage.py createsuperuser
```

3. **Follow the prompts** to set up your username, email, and password

4. **Log in to the admin interface** at http://localhost:8000/admin/ with your new credentials

## Database Management

### Connecting to the PostgreSQL Database

If you need to access the database directly:

1. **Connect to the PostgreSQL database** within the container:

```bash
docker compose exec db psql -U postgres -d carmanagement
```

2. **Run SQL commands** directly. Some useful PostgreSQL commands:

```sql
-- List all tables
\dt

-- View table structure
\d table_name

-- Run a query
SELECT * FROM app_branch LIMIT 5;

-- Exit PostgreSQL
\q
```

### Backing Up and Restoring Data

To back up your database:

```bash
docker compose exec db pg_dump -U postgres -d carmanagement > backup.sql
```

To restore from a backup:

```bash
cat backup.sql | docker compose exec -T db psql -U postgres -d carmanagement
```

## Troubleshooting Common Issues

### Permission Issues

If you encounter permission errors with static files or media:

1. **Check the logs** for detailed error messages:

```bash
docker compose logs web
```

2. **Make sure the volumes are properly configured** in docker-compose.yml

3. **Ensure the container has proper permissions** to create and modify files:

```bash
docker compose exec web ls -la /app/staticfiles
```

### Database Connection Issues

If the web service can't connect to the database:

1. **Check if the database service is running**:

```bash
docker compose ps
```

2. **Verify the database environment variables**:

```bash
docker compose exec web env | grep SQL
```

3. **Make sure the database has been created**:

```bash
docker compose exec db psql -U postgres -l
```

### Container Won't Start

If a container won't start:

1. **Check the Docker logs**:

```bash
docker compose logs
```

2. **Verify your docker-compose.yml file** for formatting issues

3. **Try rebuilding the container**:

```bash
docker compose down
docker compose up --build
```

### Running Specific Commands

To run a specific Django management command:

```bash
docker compose exec web python manage.py [command]
```

For example:
- Run migrations: `docker compose exec web python manage.py migrate`
- Create a new app: `docker compose exec web python manage.py startapp new_app`
- Enter Django shell: `docker compose exec web python manage.py shell`

## Appendix: Command Reference

Here's a quick reference for common Docker commands:

- **Build and start containers**:
  ```bash
  docker compose up --build
  ```

- **Start containers in the background**:
  ```bash
  docker compose up -d
  ```

- **Stop containers**:
  ```bash
  docker compose down
  ```

- **Stop containers and remove volumes**:
  ```bash
  docker compose down -v
  ```

- **View running containers**:
  ```bash
  docker compose ps
  ```

- **View container logs**:
  ```bash
  docker compose logs
  ```

- **Execute a command in a container**:
  ```bash
  docker compose exec [service] [command]
  ```

- **Restart a service**:
  ```bash
  docker compose restart [service]
  ```

- **Rebuild a specific service**:
  ```bash
  docker compose build [service]
  ```

By following this guide, you should be able to successfully dockerize and run the Car Management Replica Master application on your local machine.