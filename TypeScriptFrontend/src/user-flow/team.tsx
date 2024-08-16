import React, { useState } from 'react';
import config from '../env-config';

const teamMembers = [
    { 
        name: 'Yichen', 
        profilePic: './assets/Team/yichen.png', 
        intro: 'Backend Developer' 
    },
    { 
        name: 'Ryan', 
        profilePic: './assets/Team/ryan.jpg', 
        intro: 'Frontend Developer' 
    },
    { 
        name: 'Ian', 
        profilePic: './assets/Team/not_professional_ian.png', 
        intro: 'Full Stack / Creator of Durb' 
    },
    { 
        name: 'Akash', 
        profilePic: './assets/Team/akash.jpeg', 
        intro: 'Networking Engineer' 
    },
    {
        name: 'Bilal',
        profilePic: './assets/Team/bilal.png',
        intro: 'Frontend Developer'
    }
];

const Team: React.FC = () => {
    const [name, setName] = useState('');
    const [email, setEmail] = useState('');
    const [message, setMessage] = useState('');
    const [isSubmitting, setIsSubmitting] = useState(false);
    const [showPopup, setShowPopup] = useState(false);

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setIsSubmitting(true);

        try {
            const response = await fetch(`${config.userBackend}/send-email`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ userEmail: email, message })
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const result = await response.json();
            if (result.success) {
                setName('');
                setEmail('');
                setMessage('');
                setShowPopup(true);
            } else {
                alert(`Error: ${result.error}`);
            }
        } catch (error) {
            alert(`Error: ${error.message}`);
        } finally {
            setIsSubmitting(false);
        }
    };

    return (
        <div className="team-section">
            <h1 className="team-title">The Team</h1>
            <div className="team-container">
                {teamMembers.map((member, index) => (
                    <div key={index} className="team-member info-card">
                        <img src={member.profilePic} alt={member.name} />
                        <h3>{member.name}</h3>
                        <p>{member.intro}</p>
                    </div>
                ))}
            </div>
            <div className='contact-form'>
                <h2>Contact Us</h2>
                <form onSubmit={handleSubmit}>
                    <div>
                        <label>Your Name:</label>
                        <input
                            type="text"
                            value={name}
                            onChange={(e) => setName(e.target.value)}
                        />
                    </div>
                    <div>
                        <label>Email:</label>
                        <input
                            type="email"
                            value={email}
                            onChange={(e) => setEmail(e.target.value)}
                        />
                    </div>
                    <div>
                        <label>Message:</label>
                        <textarea
                            value={message}
                            onChange={(e) => setMessage(e.target.value)}
                        />
                    </div>
                    <button 
                        className="custom-button" 
                        type="submit"
                        disabled={isSubmitting}
                        style={{ backgroundColor: isSubmitting ? 'grey' : '' }}
                        >
                            {isSubmitting ? 'Submitting...' : 'Submit'}
                        </button>
                </form>
                {showPopup && (
                    <div className="popup">
                        <p>Thank you for your message!</p>
                        <button style={{ width: "40%" }} onClick={() => setShowPopup(false)}>Close</button>
                    </div>
                )}
            </div>
        </div>
    );
};

export default Team;