import React, { useState, useEffect } from 'react';
import { NavLink, useNavigate } from 'react-router-dom';
import '../../styles/style.css'; // Adjust path as needed
import config from '../env-config';

const Register: React.FC = () => {
    const [username, setUsername] = useState('');
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [message, setMessage] = useState('');
    const [isRegistered, setIsRegistered] = useState(false);
    const navigate = useNavigate();

    useEffect(() => {
        const token = localStorage.getItem('userToken');
        if (token) {
            navigate('/home');  // Redirect to home if token exists
        }
    }, [navigate]);

    const handleSubmit = async (event: React.FormEvent) => {
        event.preventDefault();
        setMessage(''); // Clear previous message

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
                    <input type="password" name="password" id="password" placeholder="Password" required
                        value={password} onChange={(e) => setPassword(e.target.value)} />
                    <i className="fas fa-lock"></i>
                </div>
                {!isRegistered && (
                    <ul className="password-requirements">
                    <li><i className="fas fa-info-circle"></i> Must be at least 8 characters long</li>
                    <li><i className="fas fa-info-circle"></i> Must contain an uppercase and a lowercase letter</li>
                </ul>
                )}
                {message && <p className="error-message">{message}</p>}
                <input type="submit" className="btn" value="Register" id="registerBtn"/>
            </form>
            {!isRegistered && (
                <p>Already have an account? <NavLink to="/login">Login here!</NavLink></p>
            )}
        </div>
    );
};

export default Register;
