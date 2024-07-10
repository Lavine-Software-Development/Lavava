import React, { useState, useEffect } from 'react';
import '../../styles/style.css';
import { Link } from 'react-router-dom';
import config from '../env-config';

interface ProfileData {
    userName: string;
    displayName: string;
    email: string;
    abilities: { name: string; count: number }[];
    elo: number;
    past_games: number[];
}

const Profile: React.FC = () => {
    const [profileData, setProfileData] = useState<ProfileData>({
        userName: 'Loading...',
        displayName: 'Loading...',
        email: 'Loading...',
        abilities: [], // Default to at least one empty list
        elo: 1000,
        past_games: [],
    });

    const [isEditing, setIsEditing] = useState(false);
    const [newDisplayName, setNewDisplayName] = useState(profileData.displayName);

    const handleEditClick = () => {
        setIsEditing(true);
    }

    const handleUpdateClick = () => {
        profileData.displayName = newDisplayName;
        setIsEditing(false);
    }

    useEffect(() => {
        const fetchData = async () => {
            const token = localStorage.getItem('userToken');
            try {
                const response = await fetch(`${config.userBackend}/profile`, {
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
            <div className="profile-card">
                <h2>My Profile</h2>
                <p>User Name: {profileData.userName}</p>
                <div className="display-name-container">
                    <p>Display Name: </p>
                    {isEditing ? (
                        <>
                        <input 
                            type="text" 
                            value={newDisplayName} 
                            onChange={(e) => setNewDisplayName(e.target.value)} 
                            placeholder={profileData.displayName}
                            className="edit-input"
                        />
                        <button className="save-btn" onClick={handleUpdateClick}>Update</button>
                        </>
                    ) : (
                        <p>{profileData.displayName}</p>
                    )}
                    {!isEditing && (
                        <button className="edit-btn" onClick={handleEditClick}>Edit</button>
                    )}
                </div>
                <p>Email: {profileData.email}</p>
            </div>
            <div className="info-cards">
                <div className="info-card">
                    <h2>My Deck</h2>
                    {profileData.abilities.map((item, index) => (
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