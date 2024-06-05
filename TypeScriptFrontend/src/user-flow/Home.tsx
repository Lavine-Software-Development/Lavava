import React, { useEffect, useState } from 'react';
import { Link, useNavigate } from "react-router-dom";

const Home: React.FC = () => {
    const navigate = useNavigate();
    const [selectedAbilities, setSelectedAbilities] = useState<any[]>([]);

    useEffect(() => {
        const storedAbilities = sessionStorage.getItem('selectedAbilities');
        const token = localStorage.getItem('userToken');
        if (storedAbilities) {
            setSelectedAbilities(JSON.parse(storedAbilities));
        } else if (token) {
            // Fetch abilities if user is logged in and no abilities are stored in sessionStorage
            fetch('http://localhost:5001/user_abilities', {
                headers: {
                    Authorization: `Bearer ${token}`,
                },
            })
            .then(response => response.json())
            .then(data => {
                if (data && data.abilities) {
                    const abilities = data.abilities;
                    sessionStorage.setItem('selectedAbilities', JSON.stringify(abilities));
                    setSelectedAbilities(abilities);
                }
            })
            .catch(error => {
                console.error('Failed to fetch abilities:', error);
            });
        }
    }, []);

    const handleLogout = () => {
        localStorage.removeItem('userToken');  // Clear the token from localStorage
        sessionStorage.clear();
        navigate('/login');  // Redirect the user to the login page
    };

    return (
        <div className="container" id="home">
            <h1 className="form-title">Home</h1>
            <i className="fas fa-user"><a href="profile">Profile</a></i>
            {selectedAbilities.length > 0 ? (
                <>
                    <input type="submit" className="btn" value="Play" onClick={() => navigate('/play')} />
                    <ul>
                        {selectedAbilities.map((ability, index) => (
                            <li key={index}>{ability.name} - Count: {ability.count}</li>
                        ))}
                    </ul>
                </>
            ) : null}
            <input type="submit" className="btn" value={selectedAbilities.length > 0 ? "Edit Deck" : "Build Deck"} onClick={() => navigate('/builder')} />
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
            <input type="submit" className="btn" value="Log Out" onClick={handleLogout} />
        </div>
    );
};

export default Home;
