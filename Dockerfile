FROM ubuntu:20.04

# Set environment variables
ENV DEBIAN_FRONTEND=noninteractive

# Install dependencies
RUN apt-get update && apt-get install -y \
    python3.9 \
    python3.9-venv \
    python3.9-dev \
    mysql-server \
    default-libmysqlclient-dev \
    && rm -rf /var/lib/apt/lists/*

# Set up Python virtual environment
RUN python3.9 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Copy requirement.txt file and install dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy .env file
COPY app/.env /app/.env


# Set up MySQL
COPY setup.sql /docker-entrypoint-initdb.d/
RUN service mysql start && \
    export $(cat /app/.env | xargs) && \
    mysql -u root -e "source /docker-entrypoint-initdb.d/setup.sql" && \
    mysql -u root -e "CREATE USER IF NOT EXISTS '$SQL_USERNAME'@'localhost' IDENTIFIED BY '$SQL_PASS'; GRANT ALL PRIVILEGES ON zappos.* TO '$SQL_USERNAME'@'localhost'; FLUSH PRIVILEGES;"
# Make home directory so SQL doesn't throw a fit
RUN usermod -d /var/lib/mysql/ mysql

# Copy Python scripts
COPY app/ /app/

# Run Python scripts
CMD ["sh", "-c", "service mysql start && export $(cat /app/.env | xargs) && python /app/populate_db.py && python /app/main.py"]