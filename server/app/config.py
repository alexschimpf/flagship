import os


MONGODB_CONN_STR = os.getenv(
    'MONGODB_CONN_STR',
    'mongodb://root:root@localhost:27017'
)
