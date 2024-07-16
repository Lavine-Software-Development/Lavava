import React, { useState, useEffect } from 'react';
import '../../styles/style.css';
import { Link, useNavigate } from 'react-router-dom';
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
    const navigate = useNavigate();
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
    const [popupMessage, setPopupMessage] = useState('');
    const [showPopup, setShowPopup] = useState(false);


    const handleLogout = () => {

        
        localStorage.removeItem("userToken");
        sessionStorage.clear();
        navigate("/login");
    };

    const handleEditClick = () => {
        setIsEditing(true);
        setNewDisplayName('');
        setPopupMessage('');
        setShowPopup(false);
    }

    const handleUpdateClick = () => {
        if (newDisplayName.trim() === '' || newDisplayName.length < 5) {
            setPopupMessage('Display name must be at least 5 characters long');
            setShowPopup(true);
            return;
        }

        fetch(`${config.userBackend}/update_display_name`, {
            method: 'POST', // use POST to send the data
            headers: {
                'Content-Type': 'application/json',
                Authorization: `Bearer ${localStorage.getItem('userToken')}`,
            },
            body: JSON.stringify({
                newDisplayName: newDisplayName,
            }),
        })
            .then((response) => response.ok)
            .then((ok) => {
                if (ok) {
                    // Update the displayName in the profileData state
                    setProfileData(prevData => ({
                        ...prevData,
                        displayName: newDisplayName,
                    }));
                    setIsEditing(false);
                    setPopupMessage('');
                    setShowPopup(false);
                }
            })
            .catch((error) => {
                console.error("Failed to update the user display name", error);
            });
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
                <p><Link to="/login">Login here</Link> to see profile data.</p>
            </div>
        );
    }

    return (
        <div className="dashboard-container" id="dashboard-container">
            <div className="profile-card linear-gradient">
                <h2 className="text-shadow">Profile</h2>
                <p className="whiteText"><span className="text-shadow">User Name:</span> {profileData.userName}</p>
                <div className="display-name-container">
                    <p className="whiteText text-shadow">{!isEditing ? 'Display Name:' : 'New Name:'}</p>
                    {isEditing ? (
                        <>
                            <input 
                                type="text" 
                                value={newDisplayName} 
                                onChange={(e) => setNewDisplayName(e.target.value)} 
                                placeholder={profileData.displayName}
                                className="edit-input"
                            />
                            <button className="update-btn" onClick={handleUpdateClick}>Update</button>
                            {showPopup && 
                            <div className="popup">
                                <span>{popupMessage}</span>
                                <button onClick={() => setShowPopup(false)}>Close</button>
                            </div>
                            }
                        </>
                    ) : (
                        <p className="whiteText">{profileData.displayName}</p>
                    )}
                    {!isEditing && (
                        <button className="edit-btn" onClick={handleEditClick}>Edit</button>
                    )}
                </div>
                <p className="whiteText"><span className="text-shadow">Email:</span> {profileData.email}</p>
                <button className="logout-btn" onClick={handleLogout}>Log Out</button>
            </div>
            <div className="info-cards">
                <div className="info-card linear-gradient">
                    <h2 className="text-shadow">Default Deck</h2>
                    {profileData.abilities.map((item, index) => (
                        <p className="whiteText" key={index}>{item.count} {item.name}</p>
                    ))}
                </div>
                <div className="info-card linear-gradient">
                    <h2><span className="text-shadow">ELO:</span> <span className="elo-value">{profileData.elo}</span></h2>
                    {profileData.past_games.map((position, index) => (
                        <p key={index}>Game {index + 1}: {position}</p>
                    ))}
                </div>
            </div>
        </div>
    );
};

export default Profile;