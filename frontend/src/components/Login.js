import axios from "axios";
import {Navigate} from "react-router-dom";
import {useState} from "react";

export const Login = () => {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [navigate, setNavigate] = useState(false);
    const [message, setMessage] = useState('');
       
    const submit = async e => {
        e.preventDefault();

        const response = await axios.post('auth/login', {
           username, password
        }, {withCredentials: true});
       
       console.log(Object.keys(response))
        if(response.status === 200){
            //console.log()
        const { token, user } = response.data;
         localStorage.setItem("token", JSON.stringify(token));
         localStorage.setItem("user", JSON.stringify(user));
         axios.defaults.headers.common['Authorization'] = `Bearer ${token.access_token}`;
      
        setNavigate(true);
       }
        else {
            console.log(response.response)
            const error_msg= response.response.data.detail[0]["msg"]?response.response.data.detail[0]["msg"]:response.response.data.detail;
            console.log(error_msg);
            setMessage(error_msg) ;   
            setNavigate(false);
                 
    }
    }

    if (navigate) {
        return <Navigate to="/"/>;
    }

    return <main className="form-signin">
        <form onSubmit={submit}>
            <h1 className="h3 mb-3 fw-normal">Please sign in</h1>
            <h6>{`${message}`}</h6>
                       
            <div className="form-floating">
                <input type="text" className="form-control" id="floatingUsername" placeholder="username"
                       onChange={e => setUsername(e.target.value)}
                />
                <label htmlFor="floatingUsername">username </label>
            </div>

            <div className="form-floating">
                <input type="password" className="form-control" id="floatingPassword" placeholder="Password"
                       onChange={e => setPassword(e.target.value)}
                />
                <label htmlFor="floatingPassword">Password</label>
            </div>

            
     
            <button className="w-100 btn btn-lg btn-primary" type="submit">Sign in</button>
        </form>
    </main>
}
