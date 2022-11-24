import axios from 'axios';

const axiosInstance = axios.create({
    baseURL: 'http://localhost:8000/',
    timeout: 0,
    headers: {
        Authorization: localStorage.getItem("auth-token")
    },
});

export default axiosInstance;