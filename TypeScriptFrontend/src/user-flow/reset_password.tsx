import React, { useState } from 'react';
import '../../styles/style.css'; // Adjust path as needed

const ForgotPassword: React.FC = () => {
    const [password, setPassword] = useState('');
    const [repeatPassword, setRepeatPassword] = useState('');

    const handleSubmit = (event: React.FormEvent) => {
        event.preventDefault();
        // Implement your password reset logic here
        console.log(password, repeatPassword);
    };

    return (
        <div className="container" id="reset-password">
            <form onSubmit={handleSubmit}>
                <h1 className="form-title">
                    Reset your password
                    <span className="form-subtitle">Enter a new password to reset your old password</span>
                </h1>
                <div className="input-group">
                    <label htmlFor="password">Enter your new password<span className="required">*</span></label>
                    <input type="password" name="password" id="password" placeholder="Password" required
                        value={password} onChange={(e) => setPassword(e.target.value)} />
                    <i className="fas fa-lock"></i>
                </div>
                <ul className="password-requirements">
                    <li><i className="fas fa-info-circle"></i> Must be at least 15 characters long</li>
                    <li><i className="fas fa-info-circle"></i> Must contain an uppercase and a lowercase letter</li>
                    <li><i className="fas fa-info-circle"></i> Must contain a number</li>
                    <li><i className="fas fa-info-circle"></i> Must contain a special character (!, %, @, #, etc.)</li>
                </ul>
                <div className="input-group">
                    <label htmlFor="repeat-password">Repeat your new password<span className="required">*</span></label>
                    <input type="password" name="repeat-password" id="repeat-password" placeholder="Repeat password" required
                        value={repeatPassword} onChange={(e) => setRepeatPassword(e.target.value)} />
                    <i className="fas fa-lock"></i>
                </div>
                <input type="submit" className="btn" value="Update Password" />
            </form>
        </div>
    );
};

export default ForgotPassword;
