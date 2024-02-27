class Flagship {
  /**
       * @param host
       * @param projectId
       * @param userKey
       * @param signature:
       *    Optional. This signature should come from a source that knows the private key.
       *    As a browser client, this should come from your application's server.
       *    This will be used by the Flagship API for authentication.
       *
       *    If this is not provided, a `privateKey` must be provided instead. This is
       *    useful when using server-side javascript where the private key is secure.
       * @param privateKey:
       *    If `signature` is not provided, a `privateKey` must be provided instead. This is
       *    useful when using server-side javascript where the private key is secure.
       * @param port
       */
  constructor (host, projectId, userKey, signature = undefined, privateKey = undefined, port = 443) {
    this.projectId = projectId
    this.userKey = userKey
    this.signature = signature
    this.host = host
    this.scheme = port === 443 ? 'https' : 'http'
    this.port = port
    this.enabledFeatureFlags = new Set()

    if (!this.signature && !privateKey) {
      throw new Error('Either signature or private key is required')
    }

    if (!this.signature && privateKey) {
      this.signature = this._generateSignature(privateKey)
    }
  }

  /**
       * Loads the latest enabled feature flags for a user, given some context.
       * This will make an async request to the Flagship API.
       * This should be used sparingly - typically only in cases where the context changes.

       * @param context
       *     If this is not provided, the context passed into the constructor will be used instead.
       * @param timeout
       *     Request timeout (in milliseconds)
       * @returns {Promise}
       */
  load = async (context, timeout = 60000) => {
    const response = await this._request(context, timeout)
    const enabledFeatureFlags = response.data.feature_flags
    this.setEnabledFeatureFlags(enabledFeatureFlags)
    return enabledFeatureFlags
  }

  /**
       * Returns whether or not a feature flag is enabled for a user, given some context
       *
       * @param name: feature flag name
       * @returns {boolean}
       */
  isFeatureFlagEnabled = (name) => {
    return this.enabledFeatureFlags.has(name)
  }

  /**
       * Returns all the enabled feature flags for a user, given some context
       */
  getEnabledFeatureFlags = () => {
    return this.enabledFeatureFlags
  }

  /**
       * This can be used to bootstrap Flagship with some initial feature flags.
       */
  setEnabledFeatureFlags = (enabledFeatureFlags) => {
    this.enabledFeatureFlags = new Set(enabledFeatureFlags)
  }

  _generateSignature = (privateKey) => {
    // TODO
  }

  _request = async (context, timeout) => {
    const params = new URLSearchParams({
      project_id: this.projectId,
      user_key: this.userKey
    })
    const url = `${this.scheme}://${this.host}:${this.port}/feature_flags?${params}`
    const headers = {
      'Content-Type': 'application/json',
      Signature: this.signature
    }
    const data = JSON.stringify({
      context
    })
    const response = await fetch(url, {
      method: 'POST',
      body: data,
      headers,
      signal: AbortSignal.timeout(timeout)
    })
    return response.json()
  }
}

export default Flagship
