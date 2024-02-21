# Overview

Flagship is a full-stack feature flag management platform.

<hr>

### Components

#### UI server

<i>Next.js / Typescript</i>

- Runs the Flagship UI

#### Admin server
<i>Python / FastAPI</i>

- API server used by the Flagship UI
- Deals with:
    - Authentication
    - Managing projects
    - Managing context fields
    - Managing feature flags
    - Mangaging users
    - Retrieving audit logs

#### Flags server
<i>Python / FastAPI</i>

- Handles determining which feature flags are enabled for a given context

#### SDKs
- Libraries for interacting with the Flags server
- SDKs are available in various programming languages

<hr>

### Databases

The Admin and Flags servers require MySQL and Redis Cluster.
