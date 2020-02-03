# dbdv2
dbdv2
1. build the docker-compose

docker-compose up


2. 
enter the main program
docker exec -it dbd_python ./start.sh

start the frontend:
docker exec -it dbd_web python3 manage.py runserver 0.0.0.0:8000



3.
http://localhost:9000/
(the front end of the program)
http://localhost:8090/
(the airflow of the program)
