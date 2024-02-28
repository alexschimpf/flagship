# Projects

<p>
    A project typically maps to a specific system, e.g. a web app or backend system.
    Within a project, you can create <a href="/feature-flags">feature flags</a> and <a href="/context-fields">context fields</a>.
    Users are assigned to one or more projects.
</p>
<p>
    The Flagship homepage lists all available projects that are assigned to the current user.
    You can easily navigate to the feature flags, context fields, and private keys from here.
    From the homepage, you can also create a new project.
</p>

<hr>

## Private Keys

<p>
    Projects can be assigned one or more private keys.
    <b>Private keys are only ever shown at the time of creation, so remember to save them some place secure!</b>
    Private keys are needed to sign requests to the <a href="/flags-api">Flags API</a>.
</p>
<p>
    All private keys for a project are active at any given time. If you want to rotate keys, simply create a new
    private key, modify your system to use it, and then delete the old one.
</p>
