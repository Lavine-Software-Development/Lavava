import React, { useEffect, useState } from 'react';
import '../../styles/style.css'; // Adjust path as needed
import config from '../env-config';
import { NavLink, useNavigate } from 'react-router-dom';

const ForgotPassword: React.FC = () => {
    const [password, setPassword] = useState('');
    const [repeatPassword, setRepeatPassword] = useState('');
    const [username, setUsername] = useState('');
    const [isLoading, setIsLoading] = useState(false); // state for loading
    const [message, setMessage] = useState('');
    const [isReset, setIsReset] = useState(false); // state for update password button
    const [noAccount, setnoAccount] = useState(false); // state for register link
    const navigate = useNavigate();

    const handleSubmit = async (event: React.FormEvent) => {
        event.preventDefault();
        setMessage(''); // Clear previous message

        // Prompt for confirmation
        const confirmed = window.confirm('Are you sure you want to reset your password?');
        if (!confirmed) {
            setIsLoading(false); // Set isLoading to false when canceled
            // Blur the button to remove focus
            const resetBtn = document.getElementById('resetBtn');
            if (resetBtn) {
                resetBtn.blur();
            }
            return;
        }

        setIsLoading(true);

        try {
            const response = await fetch(`${config.userBackend}/reset_password`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ username, password, repeatPassword })
            });
            const data = await response.json();
            if (response.ok) {
                setMessage(data.message);
                setIsReset(true);
            } else {
                setMessage(data.message);
                if (response.status == 404){
                    setnoAccount(true);
                }
            }
        } catch (error) {
            setMessage("Failed to connect to the server.");
        } finally {
            setIsLoading(false);
        }
    };

    useEffect(() => { // add register link at bottom if they enter a username or email that doesnt exist
        if (isReset) {
            const resetBtn = document.getElementById('resetBtn');
            if (resetBtn) {
                resetBtn.value = 'Login';
                resetBtn.onclick = () => navigate('/login');
            }
        }
    }, [isReset, navigate]);

    useEffect(() => {
        setnoAccount(false); // Reset noAccount state when username changes
    }, [username]);


    return (
        <div className="container" id="reset-password">
            <form onSubmit={handleSubmit}>
                <h1 className="form-title">
                    Reset your password
                    <span className="form-subtitle">Enter a new password to reset your old password</span>
                </h1>
                <div className="input-group">
                    <label htmlFor="username/email">Username/Email<span className="required">*</span></label>
                    <input type="text" name="username" id="username" placeholder="Username/Email" required
                        value={username} onChange={(e) => setUsername(e.target.value)} />
                    <i className="fas fa-user"></i>
                </div>
                <div className="input-group">
                    <label htmlFor="password">Enter your new password<span className="required">*</span></label>
                    <input type="password" name="password" id="password" placeholder="Password" required
                        value={password} onChange={(e) => setPassword(e.target.value)} />
                    <i className="fas fa-lock"></i>
                </div>
                <ul className="password-requirements">
                    <li><i className="fas fa-info-circle"></i> Must be at least 8 characters long</li>
                    <li><i className="fas fa-info-circle"></i> Must contain an uppercase and a lowercase letter</li>
                </ul>
                <div className="input-group">
                    <label htmlFor="repeat-password">Repeat your new password<span className="required">*</span></label>
                    <input type="password" name="repeat-password" id="repeat-password" placeholder="Repeat password" required
                        value={repeatPassword} onChange={(e) => setRepeatPassword(e.target.value)} />
                    <i className="fas fa-lock"></i>
                </div>
                {message && <p className="error-message">{message}</p>}
                {isLoading && <p className="loading-message">Please wait...</p>}
                <input type="submit" className="btn" value="Reset Password" id="resetBtn" disabled={isLoading}/>
                {noAccount && (
                <p>Need an account? <NavLink to="/register">Register here!</NavLink></p>
            )}
            </form>
        </div>
    );
};

export default ForgotPassword;
