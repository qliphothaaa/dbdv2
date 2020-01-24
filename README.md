# dbdv2
dbdv2
1. build the docker-compose

docker-compose up


2. enter the database

docker exec -it dbd_database_1 bash

3. load the database

mysql -u root -p < tmp/dbd.sql

password is 1234


4. enter the main program and run it

docker exec -it dbd_python_1 bash

cd dbdv2

./load_from_excel #load the excel file to database, then you can go to database and select * from dbdcompany to see result.

./crawl#start the scraping



x. test

./test
(some path ploblem. If the console say like "No module named 'dbd_connector'", please add a "." before the module name.) 
