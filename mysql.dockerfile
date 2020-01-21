FROM mysql

ENV MYSQL_ROOT_PASSWORD=1234
ENV MYSQL_USER=root
ENV MYSQL_PASSWORD=1234

COPY ./dbd.sql /tmp/dbd.sql

RUN mysql -u root -p${MYSQL_ROOT_PASSWORD}  < /tmp/dbd.sql
