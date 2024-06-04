import React, { useState, useEffect } from 'react';
import '../../styles/style.css';
import { Link } from 'react-router-dom';

interface ProfileData {
    userName: string;
    displayName: string;
    email: string;
    abilities: { name: string; count: number }[][];
    elo: number;
    past_games: number[];
}

const Profile: React.FC = () => {
    const [profileData, setProfileData] = useState<ProfileData>({
        userName: 'Loading...',
        displayName: 'Loading...',
        email: 'Loading...',
        abilities: [[]], // Default to at least one empty list
        elo: 1000,
        past_games: [],
    });
    const [selectedTab, setSelectedTab] = useState(0); // Track the currently selected tab for abilities

    useEffect(() => {
        const fetchData = async () => {
            const token = localStorage.getItem('userToken');
            try {
                const response = await fetch(`http://localhost:5001/profile`, {
                    method: 'GET',
                    headers: {
                        'Authorization': `Bearer ${token}`
                    }
                });
                const data = await response.json();
                if (response.ok) {
                    setProfileData(data);
                } else {
                    throw new Error(data.message);
                }
            } catch (error) {
                console.error('Error fetching data:', error);
            }
        };
        fetchData();
    }, []);

    if (!localStorage.getItem('userToken')) {
        return (
            <div className="container" id="dashboard-container">
                <p>Login <Link to="/login">here</Link> to see profile data.</p>
            </div>
        );
    }

    return (
        <div className="dashboard-container" id="dashboard-container">
            <i className="fas fa-user"><a href="home">Home</a></i>
            <div className="profile-card">
                <h2>My Profile</h2>
                <p>User Name: {profileData.userName}</p>
                <p>Display Name: {profileData.displayName}</p>
                <p>Email: {profileData.email}</p>
                <button className="save-btn">Update</button>
            </div>
            <div className="info-cards">
                <div className="info-card">
                    <h2>My Deck</h2>
                    <div className="tabs">
                        {profileData.abilities.map((_, index) => (
                            <button
                                key={index}
                                onClick={() => setSelectedTab(index)}
                                style={{ fontWeight: selectedTab === index ? 'bold' : 'normal' }}
                            >
                                Deck {index + 1}
                            </button>
                        ))}
                    </div>
                    {profileData.abilities[selectedTab].map((item, index) => (
                        <p key={index}>{item.count} {item.name}</p>
                    ))}
                </div>
                <div className="info-card">
                    <h2>My ELO: {profileData.elo}</h2>
                    {profileData.past_games.map((position, index) => (
                        <p key={index}>Game {index + 1}: {position}</p>
                    ))}
                </div>
            </div>
        </div>
    );
};

export default Profile;