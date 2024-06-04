import React, { useState } from 'react';
import '../../styles/style.css'; // Adjust path as needed

const Register: React.FC = () => {
    const [username, setUsername] = useState('');
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');

    const handleSubmit = (event: React.FormEvent) => {
        event.preventDefault();
        // Implement your registration logic here
        console.log(username, email, password);
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
                    <input type="text" name="email" id="email" placeholder="Email" required
                        value={email} onChange={(e) => setEmail(e.target.value)} />
                </div>
                <div className="input-group">
                    <label htmlFor="password">Password</label>
                    <input type="password" name="password" id="password" placeholder="Password" required
                        value={password} onChange={(e) => setPassword(e.target.value)} />
                </div>
                <input type="submit" className="btn" value="Register" />
            </form>
            <p>Already have an account? <a href="login">Login here!</a></p>
        </div>
    );
};

export default Register;
