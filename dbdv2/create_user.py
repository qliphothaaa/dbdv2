import airflow
from airflow import models, settings
from airflow.contrib.auth.backends.password_auth import PasswordUser

user = PasswordUser(models.User())
user.username = 'admin2'
user.email = 'asdf@example.com'
user.password = '12345'
session = settings.Session()
session.add(user)
session.commit()
session.close()
