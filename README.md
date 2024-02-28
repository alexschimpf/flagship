# Overview

Flagship is a full-stack feature flag management platform.

The <b>full</b> documentation can be found at: https://alexschimpf.github.io/flagship.

<hr>

## How It Works

<p>
    Flagship provides an intuitive web application to manage your feature flags.
</p>
<p>
    A <b>project</b> typically maps to a specific system, e.g. a web app or backend system.
</p>
<p>
Within a project, you can create <b>feature flags</b>.
You can configure feature flags to only be enabled under certain conditions.
</p>
<p>
You can also create <b>context fields</b> within a project.
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
The Flagship web application also allows you to effectively manage <b>users</b> within the platform.
Users must be invited from within Flagship.
Each user is given a role and is assigned to one or more projects.
The following roles are available (in order of increasing permissions): read only, standard, admin, and owner.
</p>

<hr>

## Example

You can find a complete example project using the Flagship platform <a href="https://github.com/alexschimpf/flagship-example">here</a>.

<hr>

## Components

#### <a href="https://alexschimpf.github.io/flagship/ui">UI Server</a>
- Runs the Flagship UI

#### <a href="https://alexschimpf.github.io/flagship/admin-api">Admin API</a>
- API server used by the Flagship UI
- Deals with:
    - Login / Authentication
    - Managing projects
    - Managing context fields
    - Managing feature flags
    - Managing users
    - Reading/writing audit logs
    - etc.

#### <a href="https://alexschimpf.github.io/flagship/flags-api">Flags API</a>
- Handles determining which feature flags are enabled for a given context
- This is what your system will be interacting with
