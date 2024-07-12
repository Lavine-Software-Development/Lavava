import React, { useState } from 'react';

const teamMembers = [
    { 
        name: 'Ryan', 
        profilePic: '../images/Team/ian_lavine.jpeg', 
        intro: 'Frontend Developer' 
    },
    { 
        name: 'Ian', 
        profilePic: '../images/Team/ian_lavine.jpeg', 
        intro: 'Backend Developer' 
    },
    { 
        name: 'Akash', 
        profilePic: '../images/Team/ian_lavine.jpeg', 
        intro: 'Networking Engineer' 
    }
];

const Team: React.FC = () => {
    const [name, setName] = useState('');
    const [email, setEmail] = useState('');
    const [message, setMessage] = useState('');

    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault();
        // Handle form submission logic here
        console.log('Contact Us form submitted:', { name, email, message });
    };

    return (
        <div class="team-section">
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
                    <button className="custom-button" type="submit">Submit</button>
                </form>
            </div>
        </div>
    );
};

export default Team;