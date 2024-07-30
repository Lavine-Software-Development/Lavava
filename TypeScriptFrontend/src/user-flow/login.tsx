import React, { useState, useEffect } from "react";
import { NavLink, useNavigate } from 'react-router-dom';
import "../../styles/style.css"; // Adjust the path as necessary
import config from '../env-config';

interface LoginProps {
  // Add any props here if needed, for example, a login function prop
}

const Login: React.FC<LoginProps> = () => {
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const [error, setError] = useState("");
    const [isLoading, setIsLoading] = useState(false); // New state for loading
    const [showPassword, setShowPassword] = useState(false);
    const [maskedPassword, setMaskedPassword] = useState("");
    const navigate = useNavigate();

    const togglePasswordVisibility = () => {
        setShowPassword(!showPassword);
    }

    const handlePasswordChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        setPassword(e.target.value);
    };

    useEffect(() => {
        const token = localStorage.getItem('userToken');
        if (token) {
            navigate('/home');  // Redirect to home if token exists
        }
        // Update masked password whenever the actual password changes
        setMaskedPassword(password.replace(/./g, '•'));
    }, [navigate, password]);

    const generateGuestToken = () => {
        return Math.random().toString(36).substring(2, 15) + Math.random().toString(36).substring(2, 15);
    };

    const handleGuestLogin = () => {
        const guestToken = generateGuestToken();
        sessionStorage.setItem('guestToken', guestToken);
        localStorage.removeItem("userToken");
        navigate('/home');
    };

    const handleSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
        event.preventDefault();
        setError(""); // Clear previous errors
        setIsLoading(true); // Start loading

        try {
            const response = await fetch(`${config.userBackend}/login`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ username, password })
            });
            const data = await response.json();
            if (response.ok) {
                localStorage.setItem('userToken', data.token);
                sessionStorage.removeItem("guestToken");
                sessionStorage.clear();
                navigate('/home');
            } else {
                setError(data.message);
            }
        } catch (err) {
            setError("Failed to connect to the server.");
        } finally {
            setIsLoading(false); // Stop loading
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
                    <div className="password-input-wrapper">
                        <input
                            type="password"
                            name="password"
                            id="password-masked"
                            placeholder="Password"
                            required
                            value={password}
                            onChange={handlePasswordChange}
                            style={{ display: showPassword ? 'none' : 'block' }}
                        />
                        <input
                            type="text"
                            name="password-visible"
                            id="password-visible"
                            placeholder="Password"
                            required
                            value={password}
                            onChange={handlePasswordChange}
                            style={{ display: showPassword ? 'block' : 'none' }}
                        />
                        <button
                            type="button"
                            className="password-toggle"
                            onClick={togglePasswordVisibility}
                        >
                            <img 
                                src={showPassword ? './assets/eye-off.png' : './assets/eye.png'} 
                                alt={showPassword ? "Hide password" : "Show password"}
                                className="eye-icon"
                            />
                        </button>
                    </div>
                </div>
                {error && <div className="error-message">{error}</div>}
                {isLoading && <p className="loading-message">Please wait...</p>}
                <NavLink to="/forgot-password" className="forgot-password">Forgot password?</NavLink>
                <input type="submit" className="btn" value="Sign In" name="Sign In" disabled={isLoading} />
                <input type="button" className="btn" value="Play as Guest" name="Play as Guest" onClick={handleGuestLogin} disabled={isLoading} />
            </form>
            <p>Don't have an account? <NavLink to="/register">Register here!</NavLink></p>
        </div>
    );
};

export default Login;
