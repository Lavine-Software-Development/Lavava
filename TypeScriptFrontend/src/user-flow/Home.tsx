import React from 'react';
// import '../../styles/style.css'; // Adjust path as needed
import { Link, useNavigate } from "react-router-dom";

const Home: React.FC = () => {
    const navigate = useNavigate();

    const handleLogout = () => {
        localStorage.removeItem('userToken');  // Clear the token from localStorage
        sessionStorage.clear();
        navigate('/login');  // Redirect the user to the login page
    };

    return (
        <div className="container" id="home">
            <h1 className="form-title">Home</h1>
            <i className="fas fa-user"><a href="profile">Profile</a></i>
            <input type="submit" className="btn" value="Play" onClick={() => navigate('/play')} />
            <input type="submit" className="btn" value="Build" onClick={() => navigate('/builder')} />
                <nav
                    style={{
                        backgroundColor: "#f0f0f0",
                        padding: "10px 0",
                        borderBottom: "2px solid #ccc",
                        marginBottom: "20px",
                    }}
                >
                    <div
                        style={{
                            display: "flex",
                            justifyContent: "center",
                            gap: "20px",
                        }}
                    >
                        <Link
                            to="/websocket-test"
                            style={{
                                padding: "10px 20px",
                                textDecoration: "none",
                                color: "#333",
                                fontWeight: "bold",
                            }}
                        >
                            WebSocket Test
                        </Link>
                    </div>
                    <div>
                    </div>
                </nav>
                <input type="submit" className="btn" value="Log Out" onClick={handleLogout} />
        </div>
    );
};

export default Home;
