import axios from 'axios';
import Cookies from 'js-cookie';
import { APIClient } from './client/APIClient';

axios.defaults.headers.put['Content-Type'] = 'application/json';
axios.defaults.headers.post['Content-Type'] = 'application/json';

const apiClient = new APIClient({
    BASE: 'http://localhost:8000'
});

// Add a request interceptor to include JWT header
axios.interceptors.request.use(
    (conf: any) => {
        // eslint-disable-next-line no-param-reassign
        conf.headers = {
            ...(conf.headers || {}),
            Authorization: `Bearer ${Cookies.get('fs-access-token') || ''}`
        };
        return conf;
    },
    (error) => Promise.reject(error)
);

export default apiClient;
