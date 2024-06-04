import React, { useState } from "react";
import { useNavigate } from 'react-router-dom';
import "../../styles/style.css"; // Adjust the path as necessary

interface LoginProps {
  // Add any props here if needed, for example, a login function prop
}

const Login: React.FC<LoginProps> = () => {
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const navigate = useNavigate();

    const handleSubmit = (event: React.FormEvent<HTMLFormElement>) => {
        event.preventDefault();
        console.log("Login Attempt:", username, password);
        // Implement your login logic here
    };

    return (
        <div className="container" id="login">
            <h1 className="form-title">
                Welcome back
                <span className="form-subtitle">Login to your account</span>
            </h1>
            <form onSubmit={handleSubmit}>
                <div className="input-group">
                    <label htmlFor="username">Username</label>
                    <input
                        type="text"
                        name="username"
                        id="username"
                        placeholder="Username/Email"
                        required
                        value={username}
                        onChange={(e) => setUsername(e.target.value)}
                    />
                    <i className="fas fa-user"></i>
                </div>
                <div className="input-group">
                    <label htmlFor="password">Password</label>
                    <input
                        type="password"
                        name="password"
                        id="password"
                        placeholder="Password"
                        required
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                    />
                    <i className="fas fa-lock"></i>
                </div>
                <a href="forgot-password" className="forgot-password">Forgot password?</a>
                <input type="submit" className="btn" value="Sign In" name="Sign In" />
                <input
                    type="button"
                    className="btn"
                    value="Play as Guest"
                    name="Play as Guest"
                    onClick={() => navigate('/home')}
                />
            </form>
            <p>Don't have an account? <a href="register"> Register here!</a></p>
        </div>
    );
};

export default Login;
