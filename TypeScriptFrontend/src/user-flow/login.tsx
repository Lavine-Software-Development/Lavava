import React, { useState, useEffect } from "react";
import { NavLink, useNavigate } from 'react-router-dom';
import "../../styles/style.css"; // Adjust the path as necessary

interface LoginProps {
  // Add any props here if needed, for example, a login function prop
}

const Login: React.FC<LoginProps> = () => {
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const [error, setError] = useState("");
    const navigate = useNavigate();

    useEffect(() => {
        const token = localStorage.getItem('userToken');
        if (token) {
            navigate('/home');  // Redirect to home if token exists
        }
    }, [navigate]);

    const handleSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
        event.preventDefault();
        setError(""); // Clear previous errors

        try {
            const response = await fetch('http://localhost:5001/login', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ username, password })
            });
            const data = await response.json();
            if (response.ok) {
                localStorage.setItem('userToken', data.token);
                sessionStorage.clear();
                navigate('/home');
            } else {
                setError(data.message);
            }
        } catch (err) {
            setError("Failed to connect to the server.");
        }
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
                {error && <div className="error-message">{error}</div>}
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
            <p>Don't have an account? <NavLink to="/register">Register here!</NavLink></p>
        </div>
    );
};

export default Login;
