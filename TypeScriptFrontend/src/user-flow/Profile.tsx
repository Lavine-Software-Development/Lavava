import React, { useState, useEffect } from 'react';
import '../../styles/style.css'; // Ensure the path to your CSS file is correct

interface ProfileData {
    userName: string;
    displayName: string;
    email: string;
    abilities: string[];
    elo: number
    past_games: number[];
}

const Profile: React.FC = () => {
    const [profileData, setProfileData] = useState<ProfileData>({
        userName: 'Loading...',
        displayName: 'Loading...',
        email: 'Loading...',
        abilities: [],
        elo: 1000,
        past_games: [],
    });

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

    return (
        <div className="dashboard-container" id="dashboard-container">
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
                    {profileData.abilities.map((ability, index) => (
                        <p key={index}>{ability}</p>
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
