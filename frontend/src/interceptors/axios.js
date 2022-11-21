import axios from "axios";

axios.defaults.baseURL = 'http://localhost:8000/api/';

let refresh = false;

axios.interceptors.response.use(resp => resp, async error => {
    if (error.response.status === 401 && !refresh) {
        refresh = true;
        
        const storedToken = JSON.parse(localStorage.getItem("token"));
        axios.defaults.headers.common['Authorization'] = `Bearer ${storedToken.refresh_token}`;
        const response = await axios.post('auth/refresh', {}, {withCredentials: true});

        if (response.status === 200) {
         const { token, user } = response.data;
         localStorage.setItem("token", JSON.stringify(token));
         localStorage.setItem("user", JSON.stringify(user));
         axios.defaults.headers.common['Authorization'] = `Bearer ${token.access_token}`;

            return axios(error.config);
        }
    }
    refresh = false;
    return error;
});
