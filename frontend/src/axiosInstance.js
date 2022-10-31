import axios from 'axios';

const baseURL = 'http://${window.location.hostname}:8000/api/';

const axiosInstance = axios.create({
    baseURL
});

export default axiosInstance;