import axios from 'axios';
import Cookies from "js-cookie";

const csrftoken = Cookies.get('csrftoken');

const axiosInstance = axios.create({
    baseURL: 'http://localhost:8080/',
    timeout: 5000,
    headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': csrftoken
    }
});

export default axiosInstance;