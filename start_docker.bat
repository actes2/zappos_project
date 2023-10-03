@echo off
echo "Starting docker container and passing port 80:80!"
docker run -t -d -p 80:80 zappos_project_actes
start http://127.0.0.1/