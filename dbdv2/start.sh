#!/bin/bash

airflow initdb
airflow webserver
python create_user.py

