# Admin API

The Flagship UI uses the Admin API to do the following types of things:
- Login / Authentication
- Managing projects
- Managing context fields
- Managing feature flags
- Managing users
- Reading/writing audit logs
- etc.

<hr>

## Infrastructure

The Admin API is written in Python 3.12 and runs on FastAPI.

<hr>

## Dependencies

The only external dependencies for the Admin API is Redis Cluster and MySQL.
Redis Cluser stores cached data related to projects and feature flags.
MySQL stores everything else.

<hr>

## Authentication

Authentication is done via JWT cookies assigned at login.

<hr>

## Authorization

All endpoints have the necessary role-based permissions checks.
User roles are described on the <a href="/users">Users</a> page.

<hr>

## Installation

You can use the following Docker image from Dockerhub:

```
alexschimpf/flagship-admin:latest
```

You can read more about configuring this server in <a href="/installation">Installation</a>.
