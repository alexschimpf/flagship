import os


SECRET_KEY = os.getenv('SECRET_KEY', '_NOR3QX7-7LAJLLQ_OeOMuFzfq1Xg9RICwTalktXg5s=')
MYSQL_CONN_STR = os.getenv('MYSQL_CONN_STR', 'mysql+mysqlconnector://root:test@localhost:3306/flagship')
MYSQL_ECHO = os.getenv('MYSQL_ECHO', True)
MYSQL_ISOLATION_LEVEL = os.getenv('MYSQL_ISOLATION_LEVEL', 'READ COMMITTED')
MYSQL_POOL_SIZE = os.getenv('MYSQL_POOL_SIZE', 5)
MYSQL_MAX_OVERFLOW = os.getenv('MYSQL_MAX_OVERFLOW', 10)
