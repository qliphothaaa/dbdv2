#!/bin/bash

airflow initdb
airflow scheduler -D
airflow webserver

