# Overview

Flagship is a full-stack feature flag management platform.

<hr>

## How It Works

<p>
    Flagship provides an intuitive web application to manage your feature flags.
</p>
<p>
    A <a href="/flagship/projects">project</a> typically maps to a specific system, e.g. a web app or backend system.
</p>
<p>
Within a project, you can create <a href="/flagship/feature-flags">feature flags</a>.
You can configure feature flags to only be enabled under certain conditions.
</p>
<p>
You can also create <a href="/flagship/context-fields">context fields</a> within a project.
Context fields describe the context when resolving which feature flags are enabled.
For example, suppose you have a website that you want to control with feature flags.
When you ask the Flagship API to determine which feature flags are enabled for the current user, you need to describe
the user to Flagship. So you may do this by providing the following context fields to Flagship: `user_id` and `country_code`.
You would create a separate context field for each and tell Flagship their types (i.e. integer and string).
You can then use these context fields in your feature flag conditions. For example, you could have conditions like:

```
(
    `user_id` is one of [1,2,3] AND
    `country_code` is not "US"
) OR
(
    `country_code` is "US"
)
```

Context fields can be assigned the following types: integer, number, string, boolean, semantic version, integer list, string list, and enum list.
</p>
<p>
Most operations done via the UI are recorded via audit logs. For example, you can see a history of changes
for a particular feature flag.
</p>
<p>
The Flagship web application also allows you to effectively manage <a href="/flagship/users">users</a> within the platform.
Users must be invited from within Flagship.
Each user is given a role and is assigned to one or more projects.
The following roles are available (in order of increasing permissions): read only, standard, admin, and owner.
</p>

<hr>

## Getting Started

### Running From Source

To run Flagship from source, follow these steps:

1. Make sure you have the latest version of <a href="https://docs.docker.com/engine/install/">Docker</a> installed and running
1. `git clone git@github.com:alexschimpf/flagship.git`
2. `cd flagship`
1. `make -C docker flagship`
    - This will run the UI server, Admin API, Flags API, MySQL, and Redis Cluster via docker-compose
1. Open <a href="https://localhost:3000">https://localhost:3000</a> in your browser
1. Log in with user `owner@flag.ship` and password: `Test123!`

### Production

To run Flagship in production, you can use the following images from Dockerhub:

<table>
    <tr>
        <th>Name</th>
        <th>Image</th>
    </tr>
    <tr>
        <td>UI Server</td>
        <td>alexschimpf/flagship-frontend:latest</td>
    <tr>
    <tr>
        <td>Admin API</td>
        <td>alexschimpf/flagship-admin:latest</td>
    <tr>
    <tr>
        <td>Flags API</td>
        <td>alexschimpf/flagship-flags:latest</td>
    <tr>
</table>

To configure these appropriately, please read <a href="/flagship/installation">Installation</a>.
To learn more about connecting your system to Flagship, please read <a href="/flagship/sdk">SDK</a>.

<hr>

## Example

You can find a complete example project using the Flagship platform <a href="https://github.com/alexschimpf/flagship-example">here</a>.

<hr>

## Components

#### <a href="/flagship/ui">UI Server</a>
- Runs the Flagship UI

#### <a href="/flagship/admin-api">Admin API</a>
- API server used by the Flagship UI
- Deals with:
    - Login / Authentication
    - Managing projects
    - Managing context fields
    - Managing feature flags
    - Managing users
    - Reading/writing audit logs
    - etc.

#### <a href="/flagship/flags-api">Flags API</a>
- Handles determining which feature flags are enabled for a given context
- This is what your system will be interacting with


## Screenshots

#### Homepage
![Homepage](images/homepage.png)

#### Members
![Members](images/members.png)

#### Project Private Keys
![Project private keys](images/private-keys.png)

#### System Audit Logs
![System audit logs](images/system-audit-logs.png)

#### Feature Flags
![Feature flags](images/feature-flags.png)

#### Edit Feature Flag
![Edit feature flag](images/edit-feature-flag.png)

#### Feature Flag Audit Logs
![Feature flag audit logs](images/feature-flag-audit-logs.png)

#### Context Fields
![Context fields](images/context-fields.png)

#### Edit Context Field
![Edit context field](images/edit-context-field.png)

#### Context Field Audit Logs
![Context field audit logs](images/context-field-audit-logs.png)

#### Light Mode
![Light mode](images/light-mode.png)
