import React, { useState, useEffect, useRef } from 'react';
import { NavLink, useNavigate } from 'react-router-dom';
import '../../styles/style.css';
import config from '../env-config';

const Register: React.FC = () => {
    const [username, setUsername] = useState('');
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [showPassword, setShowPassword] = useState(false);
    const [message, setMessage] = useState('');
    const [isRegistered, setIsRegistered] = useState(false);
    const [isLoading, setIsLoading] = useState(false);
    const navigate = useNavigate();
    const toggleButtonRef = useRef<HTMLButtonElement>(null);

    useEffect(() => {
        const token = localStorage.getItem('userToken');
        if (token) {
            navigate('/home');
        }
    }, [navigate]);

    const handleSubmit = async (event: React.FormEvent) => {
        event.preventDefault();
        setMessage('');
        setIsLoading(true);

        try {
            const response = await fetch(`${config.userBackend}/register`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ username, email, password })
            });
            const data = await response.json();
            if (response.ok) {
                setMessage(data.message);
                setIsRegistered(true);
            } else {
                setMessage(data.message);
            }
        } catch (error) {
            setMessage("Failed to connect to the server.");
        } finally {
            setIsLoading(false);
        }
    };

    useEffect(() => {
        if (isRegistered) {
            const registerBtn = document.getElementById('registerBtn');
            if (registerBtn) {
                registerBtn.value = 'Login';
                registerBtn.onclick = () => navigate('/login');
            }
        }
    }, [isRegistered, navigate]);

    const togglePasswordVisibility = () => {
        setShowPassword(!showPassword);
    };

    useEffect(() => {
        const ensureCustomIconVisibility = () => {
            if (toggleButtonRef.current) {
                toggleButtonRef.current.style.display = 'block';
                toggleButtonRef.current.style.visibility = 'visible';
                toggleButtonRef.current.style.pointerEvents = 'auto';
            }
        };

        ensureCustomIconVisibility();
        const intervalId = setInterval(ensureCustomIconVisibility, 1000);

        return () => clearInterval(intervalId);
    }, []);

    return (
        <div className="container" id="register">
            <h1 className="form-title">Register</h1>
            <form onSubmit={handleSubmit}>
                <div className="input-group">
                    <label htmlFor="username">Username</label>
                    <input type="text" name="username" id="username" placeholder="Username" required
                        value={username} onChange={(e) => setUsername(e.target.value)} />
                    <i className="fas fa-user"></i>
                </div>
                <div className="input-group">
                    <label htmlFor="email">Email</label>
                    <input type="text" name="email" id="email" placeholder="Email" required
                        value={email} onChange={(e) => setEmail(e.target.value)} />
                    <i className="fas fa-envelope"></i>
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
                            onChange={(e) => setPassword(e.target.value)}
                            style={{ display: showPassword ? 'none' : 'block' }}
                        />
                        <input
                            type="text"
                            name="password-visible"
                            id="password-visible"
                            placeholder="Password"
                            required
                            value={password}
                            onChange={(e) => setPassword(e.target.value)}
                            style={{ display: showPassword ? 'block' : 'none' }}
                        />
                        <button
                            ref={toggleButtonRef}
                            type="button"
                            className="password-toggle"
                            onClick={togglePasswordVisibility}
                        >
                            <img 
                                src={showPassword ? '../../public/assets/eye-off.png' : '../../public/assets/eye.png'} 
                                alt={showPassword ? "Hide password" : "Show password"}
                                className="eye-icon"
                            />
                        </button>
                    </div>
                </div>
                {!isRegistered && (
                    <ul className="password-requirements">
                        <li><i className="fas fa-info-circle"></i> Must be at least 8 characters long</li>
                        <li><i className="fas fa-info-circle"></i> Must contain an uppercase and a lowercase letter</li>
                    </ul>
                )}
                {message && <p className="error-message">{message}</p>}
                {isLoading && <p className="loading-message">Please wait...</p>}
                <input type="submit" className="btn" value="Register" id="registerBtn" disabled={isLoading}/>
            </form>
            {!isRegistered && (
                <p>Already have an account? <NavLink to="/login">Login here!</NavLink></p>
            )}
        </div>
    );
};

export default Register;