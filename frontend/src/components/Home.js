import {useEffect, useState} from "react";
import axios from "axios";
import {Navigate} from "react-router-dom";
import Dashboard from "./Dashboard";

export const Home = () => {
    const [name, setName] = useState('');
    const [navigate, setNavigate] = useState(false);
   
    useEffect(() => {
        (async () => {
            try {

                const storedToken = JSON.parse(localStorage.getItem("token"));
                axios.defaults.headers.common['Authorization'] = `Bearer ${storedToken.access_token}`;
               
                const {data} = await axios.get('users/me');

                setName(data.name);
            } catch (e) {
                setNavigate(true);
            }
        })();
    }, []);

    const logout = async () => {
        const storedToken = JSON.parse(localStorage.getItem("token"));
        axios.defaults.headers.common['Authorization'] = `Bearer ${storedToken.access_token}`;
        await axios.post('auth/logout', {}, {withCredentials: true});

        setNavigate(true);
    }

    if (navigate) {
        return <Navigate to="/login"/>;
    }

    return <div className="form-signin mt-5 text-center">
        <Dashboard/>

        <a href="javascript:void(0)" className="btn btn-lg btn-primary" onClick={logout}>Logout</a>
    </div>
}
