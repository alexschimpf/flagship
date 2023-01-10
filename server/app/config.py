import os

SECRET_KEY = os.getenv(
    'SECRET_KEY',
    '_NOR3QX7-7LAJLLQ_OeOMuFzfq1Xg9RICwTalktXg5s='
)

MONGODB_CONN_STR = os.getenv(
    'MONGODB_CONN_STR',
    'mongodb://root:root@localhost:27017'
)
