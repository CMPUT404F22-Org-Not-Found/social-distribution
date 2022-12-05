import axios from 'axios';

const axiosInstance = axios.create({
    baseURL: 'https://cmput404-t04.herokuapp.com/',
    timeout: 0,
    headers: {
        'Authorization': `Token ${window.localStorage.getItem("auth-token")}`
    },
});

export default axiosInstance;