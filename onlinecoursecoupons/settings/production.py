from .base import *
from unipath import Path

DEBUG=False
BASE_DIR = Path(__file__).ancestor(3)

# Production Configuration
FIREBASE_CONFIG = {
    "apiKey": "AIzaSyCvdtPMemkE6RBh8prl4h0P2kAva9PqLV0",
    "authDomain": "coupons-town.firebaseapp.com",
    "databaseURL": "https://coupons-town.firebaseio.com",
    "projectId": "coupons-town",
    "storageBucket": "coupons-town.appspot.com",
    "messagingSenderId": "511956827149",
    "appId": "1:511956827149:web:2c6f55d2030f27bd9d2944",
    "measurementId": "G-8M4ZXV2J9G",
}

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql_psycopg2',
#         'NAME': 'couponstowndb',
#         'USER': 'couponstown',
#         'PASSWORD': 'Bd$U&Rivzo&L#74ETpD6#^4%!J',
#         'HOST': 'couponstowndb-restored.cwl2fnm51fqs.us-east-1.rds.amazonaws.com',
#         'PORT': '5432',
#     }
# }
