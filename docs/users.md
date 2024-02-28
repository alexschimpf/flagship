# Users

The Flagship UI also allows you to effectively manage users within the platform.
Users must be invited from within Flagship.
Each user is given a role and is assigned to one or more projects.

## User Roles

### Read only

Read only users can view feature flags. They have the lowest level of permissions.

### Standard

Standard users can manage feature flags and context fields.

### Admin

Admins can do anything except delete projects and project private keys.

### Owner

Owners can do <b>anything</b>.
There should always be at least one owner.

## Initial Setup

When you first launch Flagship, you need at least one owner to start with. From there, you can invite as many users as you need.

If you're using the docker-compose setup, the database has a default owner user with the following credentials:

<table>
    <tr>
        <th>Username</th>
        <th>Password</th>
    </tr>
    <tr>
        <td>owner@flag.ship</td>
        <td>Test123!</td>
    <tr>
</table>

If you're connecting Flagship to your own database (and have already created the necessary tables), you can add this user by running the following query:

```sql
INSERT INTO flagship.users
(
    email,
    name,
    role,
    status,
    password
)
VALUES
(
    'owner@flag.ship',
    'Flagship Owner',
    20,
    2,
    '$2a$12$Qwux2dsu.moP5dLszwxJ5uWbPy59UY1PPnoraat/lFh35ZbpZ7SLq'
);
```

You can read more about this in <a href="/flagship/installation">Installation</a>.

## Passwords

Passwords must have:

- At least 8 characters
- At least one uppercase character
- At least one lowercase character
- At least one special character
- At least one number

The Flagship UI allows you to reset your password from the login page.
