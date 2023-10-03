FROM ubuntu:latest
ADD app /app/
COPY requirements.txt /app/
ENV SQL_USERNAME="demo"
ENV SQL_PASS="!!password123%%"
ENV HOST="actesco.org"
ENV DATABASE="zappos"
ENV SESSION_KEY="super Secret Stuff"
ENV sql_username="demo"
ENV sql_pass="!!password123%%"
ENV host="actesco.org"
ENV database="zappos"
ENV session_key="super Secret Stuff"
RUN apt-get update && \
apt-get install pip -f -y && \
pip install -r /app/requirements.txt

CMD [ "python3", "./app/main.py" ]