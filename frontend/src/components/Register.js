import {useState} from "react";
import axios from "axios";
import {Navigate} from 'react-router-dom';

export const Register = () => {
    const [name, setName] = useState('');
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [passwordConfirm, setPasswordConfirm] = useState('');
    const [message, setMessage] = useState('');
   
    const [navigate, setNavigate] = useState(false);

    const submit = async e => {
        e.preventDefault();

        const response= await axios.post('auth/register', {
            name, username, password, passwordConfirm
        });
        console.log(Object.keys(response))
       
       if(response.status===201){
        setMessage("");
        setNavigate(true);
       }
       else{
        console.log(response.response)
            const error_msg= response.response.data.detail[0]["msg"]?response.response.data.detail[0]["msg"]:response.response.data.detail;
            console.log(error_msg);
            setMessage(error_msg) ;   
            setNavigate(false);
            
       }
    }

    if (navigate) {
        return <Navigate to="/login"/>;
    }

    return <main className="form-signin">
        <form onSubmit={submit}>
            <h1 className="h3 mb-3 fw-normal">Please register</h1>
            <h6>{`${message}`}</h6>
            <div className="form-floating">
                <input type="text" className="form-control" id="floatingName" placeholder="Name"
                       onChange={e => setName(e.target.value)}
                />
                <label htmlFor="floatingName">Name</label>
            </div>

            <div className="form-floating">
                <input type="text" className="form-control" id="floatingUsername" placeholder="username"
                       onChange={e => setUsername(e.target.value)}
                />
                <label htmlFor="floatingUsername">username</label>
            </div>

            <div className="form-floating">
                <input type="password" className="form-control" id="floatingPassword" placeholder="Password"
                       onChange={e => setPassword(e.target.value)}
                />
                <label htmlFor="floatingPassword">Password</label>
            </div>

            <div className="form-floating">
                <input type="password" className="form-control" id="floatingpasswordConfirm" placeholder="Confirm Password"
                       onChange={e => setPasswordConfirm(e.target.value)}
                />
                <label htmlFor="floatingpasswordConfirm">Confirm Password</label>
            </div>


            <button className="w-100 btn btn-lg btn-primary" type="submit">Submit</button>
        </form>
    </main>
}
