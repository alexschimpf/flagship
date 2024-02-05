import axios from 'axios/index';


class Flagship {

    /**
     * @param host
     * @param projectId
     * @param userKey
     * @param signature:
     *     This signature should come from a source that knows the secret key.
     *     As a browser client, this should come from your application's server.
     *     This will be used by the Flagship API for authentication.
     * @param port
     */
    constructor(host, projectId, userKey, signature, port = 443) {
        this.projectId = projectId;
        this.userKey = userKey;
        this.signature = signature;
        this.host = host;
        this.scheme = port == 443 ? 'https' : 'http';
        this.port = port;

        this.enabledFeatureFlags = new Set();

        this.load = this.load.bind(this);
        this._request = this._request.bind(this);
        this.setEnabledFeatureFlags = this.setEnabledFeatureFlags.bind(this);
        this.isFeatureFlagEnabled = this.isFeatureFlagEnabled.bind(this);
        this.getEnabledFeatureFlags = this.getEnabledFeatureFlags.bind(this);
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
    async load(context, timeout = 60000) {
        const response = await this._request(context, timeout);
        const enabledFeatureFlags = response.data.feature_flags;
        this.setEnabledFeatureFlags(enabledFeatureFlags);
        return enabledFeatureFlags;
    }

    _request(context, timeout) {
        const path = `api/projects/${this.projectId}/users/${this.userKey}/feature_flags`;
        const url = `${this.scheme}://${this.host}:${this.port}/${path}`;
        const headers = {
            'Content-Type': 'application/json',
            'FFM-Signature': this.signature
        };
        const data = JSON.stringify({
            context: context
        });
        return axios.post(url, data, { headers: headers, timeout: timeout });
    }

    /**
     * Returns whether or not a feature flag is enabled for a user, given some context
     *
     * @param name: feature flag name
     * @returns {boolean}
     */
    isFeatureFlagEnabled(name) {
        return this.enabledFeatureFlags.has(name);
    }

    /**
     * Returns all the enabled feature flags for a user, given some context
     */
    getEnabledFeatureFlags() {
        return this.enabledFeatureFlags;
    }

    /**
     * This can be used to bootstrap Flagship with some initial feature flags.
     */
    setEnabledFeatureFlags(enabledFeatureFlags) {
        this.enabledFeatureFlags = new Set(enabledFeatureFlags);
    }
}

export default Flagship;
