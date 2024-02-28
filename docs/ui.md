# UI

The Flagship UI lets you manage everything - projects, context fields, feature flags, and users.

<hr>

## Navigation

### Login

You must first log in using your email and password.
If you've forgotten your password, you can reset it from here.

### Top Bar
<p>
Depending on your permissions, top bar allows you to navigate to the Projects, Users, and System Audit Logs pages.

You can view the Help page by clicking the question mark button on the right side of the top bar.
You can also view your profile and log out.

If you have navigated within a project, you will see the active project's name here.

Additionally, you can switch between light and dark mode.
</p>

### Home Page
<p>
You will see a table with all projects on the home page.
From here, you can can navigate to the feature flags or context fields of each project.
</p>

<hr>

## Infrastructure

The UI server is written in Typescript and uses Tailwind CSS and Next.js.

<hr>

## Dependencies

The only external dependency of the UI is the Admin API.

<hr>

## Installation

You can use the following Docker image from Dockerhub:

```
alexschimpf/flagship-frontend:latest
```

You can read more about configuring this server in <a href="/installation">Installation</a>.
