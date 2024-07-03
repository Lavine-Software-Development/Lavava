import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import '../../styles/style.css'; // Adjust path as needed

const Register: React.FC = () => {
    const [username, setUsername] = useState('');
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [message, setMessage] = useState('');
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
            const response = await fetch('http://localhost:5001/register', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ username, email, password })
            });
            const data = await response.json();
            if (response.ok) {
                setMessage("Registration successful! Please check your email to confirm your account.");
            } else {
                setMessage(data.message);
            }
        } catch (error) {
            setMessage("Failed to connect to the server.");
        }
    };

    return (
        <div className="container" id="register">
            <h1 className="form-title">Register</h1>
            <form onSubmit={handleSubmit}>
                <div className="input-group">
                    <label htmlFor="username">Username</label>
                    <input type="text" name="username" id="username" placeholder="Username" required
                        value={username} onChange={(e) => setUsername(e.target.value)} />
                </div>
                <div className="input-group">
                    <label htmlFor="email">Email</label>
                    <input type="email" name="email" id="email" placeholder="Email" required
                        value={email} onChange={(e) => setEmail(e.target.value)} />
                </div>
                <div className="input-group">
                    <label htmlFor="password">Password</label>
                    <input type="password" name="password" id="password" placeholder="Password" required
                        value={password} onChange={(e) => setPassword(e.target.value)} />
                </div>
                {message && <p className="error-message">{message}</p>}
                <input type="submit" className="btn" value="Register" />
            </form>
            <p>Already have an account? <a href="/login">Login here!</a></p>
        </div>
    );
};

export default Register;
