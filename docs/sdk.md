# SDKs

<p>
    The Flagship SDK allows you to easily connect your system with Flagship. They are small libraries that make
    requests to the Flags API. There are currently 2 supported SDKs - one for Javascript and one for Python. It should
    be trivial to support other programming languages or use your own implementation.
</p>

<hr>

## Javascript

### Install

```shell
npm install flagship-sdk
```

### Browser Example

```js
import Flagship from 'flagship';

// Get auth signature from server
const signature = ...

/*
    Note: Your user key can be whatever you want to distinctly
    identify a user, as long as it's a string
*/
const flagship = Flagship(
    'example.com',  // host
    1,              // project id
    'user-123',     // user key
    signature       // auth signature
)

context = {
    accountId: 39,
    countryCode: 'US'
};

/*
    This should be called whenever the context changes.
    This makes a request to the Flags API.
*/
flagship.load(context);

const enabledFeatureFlags = flagship.getEnabledFeatureFlags();
```

### Server Example

```javascript
import Flagship from 'flagship';

/*
    Note: Your user key can be whatever you want to distinctly
    identify a user, as long as it's a string
*/
const flagship = Flagship(
    'example.com',  // host
    1,              // project id
    'user-123',     // user key
    null,           // no signature is needed since the private key is given below
    privateKey      // this should be kept somewhere secure
);

context = {
    accountId: 39,
    countryCode: 'US'
};

/*
    This should be called whenever the context changes.
    This makes a request to the Flags API.
*/
flagship.load(context);

const enabledFeatureFlags = flagship.getEnabledFeatureFlags();
```

<hr>

## Python

### Install

```shell
pip install flagship_sdk
```

### Example

```python

from flagship import Flagship

# Get private key from some place secure
private_key = ...

# Note: Your user key can be whatever you want to distinctly
# identify a user, as long as it's a string
flagship = Flagship(
    host='example.com',
    project_id=1,
    user_key='user-123',
    private_key=private_key
)

context = {
    account_id: 39,
    country_code: 'US'
}

# This should be called whenever the context changes.
# This makes a request to the Flags API.
flagship.load(context)

enabled_feature_flags = flagship.get_enabled_feature_flags()
```

### Generating Signatures

To generate an auth signature for Flagship, you need to know the private key.
Doing this on the browser is not secure since anyone can inspect your Javascript and see your system's private key.

To get around this, you can keep the private key securel server-side, generate the signature there, and send it to the client, without ever exposing the private key.
```python
from flagship import Flagship

def your_endpoint():
    # Get private key from some place secure
    private_key = ...

    flagship = Flagship(
        host='example.com',
        project_id=1,
        user_key='user-123',
        private_key=private_key
    )

    return {
        'signature': flagship.generate_signature()
    }
```
