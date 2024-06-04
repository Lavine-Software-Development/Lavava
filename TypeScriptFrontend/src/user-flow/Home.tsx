import React from 'react';
// import '../../styles/style.css'; // Adjust path as needed
import { Link, useNavigate } from "react-router-dom";

const Home: React.FC = () => {
    const navigate = useNavigate();
    return (
        <div className="container" id="home">
            <h1 className="form-title">Home</h1>
            <i className="fas fa-user"><a href="profile">Profile</a></i>
            <input type="submit" className="btn" value="Play" onClick={() => navigate('/')} />
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
                </nav>
        </div>
    );
};

export default Home;
