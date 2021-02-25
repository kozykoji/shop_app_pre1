from .settings import *
import os
import dj_database_url

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['shop_list_pre1.com', '.herokuapp.com']

db_from_env = dj_database_url.config(conn_max_age=600)
DATABASES['default'].update(db_from_env)