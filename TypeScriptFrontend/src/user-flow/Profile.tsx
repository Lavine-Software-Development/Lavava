import React from 'react';
import '../../styles/style.css'; // Ensure the path to your CSS file is correct

const Profile: React.FC = () => {
    // You can manage state here if you have dynamic data

    return (
        <div className="dashboard-container" id="dashboard-container">
            <div className="profile-card">
                <h2>My Profile</h2>
                <p>Random User</p>
                <p>+1-111-111-111</p>
                <p>random@gmail.com</p>
                <button className="save-btn">Save</button>
            </div>
            <div className="info-cards">
                <div className="info-card">
                    <h2>My Characters</h2>
                    {/* Additional content can be rendered here */}
                </div>
                <div className="info-card">
                    <h2>My Record</h2>
                    {/* Additional content can be rendered here */}
                </div>
            </div>
        </div>
    );
};

export default Profile;
