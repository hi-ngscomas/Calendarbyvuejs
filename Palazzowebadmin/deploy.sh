docker stop app-calendar-be
docker rm app-calendar-be
docker rmi plz/webadmin:latest
docker build --tag plz/webadmin -f dockerfile .
docker-compose -f python.yml up -d
docker logs app-calendar-be
docker ps
