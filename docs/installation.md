# Installation

There are various components to the Flagship platform that must be configured and installed appropriately.
They will be described below.

<hr>

## MySQL

All Flagship data is stored in MySQL. This is currently the only primary database that can be used.

To use your own MySQL database, you must perform the following bootstrap steps:

1. Create a `flagship` database. See <a href="https://github.com/alexschimpf/flagship/blob/main/docker/mysql/init.sh#L8">here</a>.
2. Execute the statements listed <a href="https://github.com/alexschimpf/flagship/blob/main/docker/mysql/sql/flagship.sql">here</a>.
    - This will create all necessary tables.
3. Create an initial Flagship owner user. See <a href="https://github.com/alexschimpf/flagship/blob/main/docker/mysql/sql/data.sql#L1">here</a>.
    - This will create a user with username `owner@flag.ship` and password `Test123!`.
    - You can modify the email as needed.
    - It is recommended to reset your password from the UI.

The latest MySQL version is recommended.

<hr>

## Redis Cluster

Some Flagship data is cached in Redis Cluster. This is primarily to make the Flags API faster.
The following data is stored here:

- Encrypted project private keys
- Feature flags
- Context field keys and value types

The latest Redis Cluster version is recommended.

<hr>

## Admin API

The Admin API is described in detail <a href="/flagship/admin-api">here</a>.

You can use the following Docker image from Dockerhub:

```
alexschimpf/flagship-admin:latest
```

This is the easiest way to get the Admin API up and running.

The full list of config options is defined <a href="https://github.com/alexschimpf/flagship/blob/main/admin/app/config.py#L8">here</a>.
The docker container can be configured by a number of environment variables.
If certain environment variables are not specifically defined, a warning message will be logged on startup.

<table>
    <tr>
        <th>Variable Name</th>
        <th>Notes</th>
        <th>Default</th>
    </tr>
    <tr>
        <td>SECRET_KEY</td>
        <td>Used to encrypt JWT tokens and project private keys. This should be a long random string with a length that is a multiple of 4.</td>
        <td>--</td>
    <tr>
    <tr>
        <td>MYSQL_ECHO</td>
        <td>If truthy, all MySQL statements will be logged. This should definitely be disabled in production.</td>
        <td>1</td>
    <tr>
    <tr>
        <td>MYSQL_ISOLATION_LEVEL</td>
        <td>MySQL transaction isolation level</td>
        <td>READ COMMITTED</td>
    <tr>
    <tr>
        <td>MYSQL_POOL_SIZE</td>
        <td><a href="https://docs.sqlalchemy.org/en/20/core/pooling.html#sqlalchemy.pool.QueuePool.params.pool_size">See here</a></td>
        <td>5</td>
    <tr>
    <tr>
        <td>MYSQL_MAX_OVERFLOW</td>
        <td><a href="https://docs.sqlalchemy.org/en/20/core/pooling.html#sqlalchemy.pool.QueuePool.params.max_overflow">See here</a></td>
        <td>10</td>
    <tr>
    <tr>
        <td>MYSQL_CONN_STR</td>
        <td>Should follow the following format: mysql+mysqlconnector://USER:PASSWORD@HOSTNAME:PORT/flagship</td>
        <td>--</td>
    <tr>
    <tr>
        <td>REDIS_CONN_STR</td>
        <td>Should follow the following format: redis://HOSTNAME:PORT</td>
        <td>--</td>
    <tr>
    <tr>
        <td>UI_BASE_URL</td>
        <td>The UI base URL. This should NOT end with a trailing slash.</td>
        <td>http://localhost:3000</td>
    <tr>
    <tr>
        <td>SESSION_COOKIE_KEY</td>
        <td>The login session cookie key name</td>
        <td>flagship-session</td>
    <tr>
    <tr>
        <td>SESSION_COOKIE_MAX_AGE</td>
        <td>Login session cookie max age (in seconds)</td>
        <td>86400 (i.e. 24 hours)</td>
    <tr>
    <tr>
        <td>SESSION_COOKIE_DOMAIN</td>
        <td>The domain name tied to your login session cookie</td>
        <td>localhost</td>
    <tr>
    <tr>
        <td>CORS_ALLOW_ORIGINS</td>
        <td>A comma-separated list of allowed origins for CORS. Your Flagship UI base URL should be listed here.</td>
        <td>http://localhost:3000</td>
    <tr>
    <tr>
        <td>SET_PASSWORD_TOKEN_TTL</td>
        <td>How long a password reset token lives before becoming invalid</td>
        <td>86400 (i.e. 24 hours)</td>
    <tr>
    <tr>
        <td>ENABLE_FAKE_AUTH</td>
        <td>This is used to skip authentication checks during testing. This should definitely be disabled in production.</td>
        <td>False</td>
    <tr>
    <tr>
        <td>DEFAULT_LOCALE</td>
        <td>Currently this doesn't have any effect because "en-us" is the only supported locale.</td>
        <td>en-us</td>
    <tr>
    <tr>
        <td>SMTP_HOST</td>
        <td>SMTP server hostname. Used for sending emails from Flagship.</td>
        <td>--</td>
    <tr>
    <tr>
        <td>SMTP_PORT</td>
        <td>SMTP server port. Used for sending emails from Flagship.</td>
        <td>--</td>
    <tr>
    <tr>
        <td>SMTP_USER</td>
        <td>SMTP server user. Used for sending emails from Flagship.</td>
        <td>--</td>
    <tr>
    <tr>
        <td>SMTP_PASSWORD</td>
        <td>SMTP server password. Used for sending emails from Flagship.</td>
        <td>--</td>
    <tr>
    <tr>
        <td>EMAIL_FROM_ADDRESS</td>
        <td>This is the "From" email address used for emails from Flagship. This address should be owned by you.</td>
        <td>--</td>
    <tr>
</table>

<hr>

## Flags API

The Flags API is described in detail <a href="/flagship/flags-api">here</a>.

You can use the following Docker image from Dockerhub:

```
alexschimpf/flagship-flags:latest
```

This is the easiest way to get the Flags API up and running.

The full list of config options is defined <a href="https://github.com/alexschimpf/flagship/blob/main/flags/app/config.py#L8">here</a>.
The docker container can be configured by a number of environment variables.
If certain environment variables are not specifically defined, a warning message will be logged on startup.

<table>
    <tr>
        <th>Variable Name</th>
        <th>Notes</th>
        <th>Default</th>
    </tr>
    <tr>
        <td>SECRET_KEY</td>
        <td>Used to encrypt JWT tokens and project private keys. This should be a long random string with a length that is a multiple of 4.</td>
        <td>--</td>
    <tr>
    <tr>
        <td>REDIS_CONN_STR</td>
        <td>Should follow the following format: redis://HOSTNAME:PORT</td>
        <td>--</td>
    <tr>
    <tr>
        <td>CORS_ALLOW_ORIGINS</td>
        <td>A comma-separated list of allowed origins for CORS. If you are interacting with the Flags API from a browser, this should be set to your website's base URL.</td>
        <td>http://localhost:3000</td>
    <tr>
    <tr>
        <td>DEFAULT_LOCALE</td>
        <td>Currently this doesn't have any effect because "en-us" is the only supported locale.</td>
        <td>en-us</td>
    <tr>
</table>

<hr>

## UI

The UI is described in detail <a href="/flagship/ui">here</a>.

You can use the following Docker image from Dockerhub:

```
alexschimpf/flagship-frontend:latest
```

The docker container can be configured using the following environment variables:

<table>
    <tr>
        <th>Variable Name</th>
        <th>Notes</th>
        <th>Default</th>
    </tr>
    <tr>
        <td>API_BASE_URL</td>
        <td>Base URL of the Admin API</td>
        <td>http://localhost:8000</td>
    <tr>
</table>

<hr>

## SDK

To connect your system to Flagship's Flags API, you can use an available <a href="/flagship/sdk">SDK</a>.
There are currently 2 supported SDKs - one for Javascript and one for Python. It should
be trivial to support other programming languages or use your own implementation.

<hr>

## Example Project

See an example project <a href="/flagship/example">here</a>.
