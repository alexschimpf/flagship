import { APIClient } from './client/APIClient';

const apiClient = new APIClient({
    BASE: 'http://localhost:8000'
});

export default apiClient;
