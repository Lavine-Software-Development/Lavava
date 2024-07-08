import React, { useState, useEffect } from "react";
import '../../styles/style.css';
import config from '../env-config';

const Leaderboard: React.FC = () => {
    // State to store the leaderboard data
    const [leaderboard, setLeaderboard] = useState([]);

    // Fetch the leaderboard data from the server when the component mounts
    useEffect(() => {
        fetch(`${config.userBackend}/leaderboard`)
            .then(response => response.json())
            .then(data => {
                setLeaderboard(data.leaderboard);
            })
            .catch(error => {
                console.error('Error fetching leaderboard data:', error);
            });
    }, []); // Empty array ensures this runs only once

    return (
        <div className="leaderboard-container scrollable-container">
            <h1>Leaderboard</h1>
            <ul className="leaderboard-list">
                {leaderboard.map((player: { userName: string, elo: number }, index: number) => (
                    <li key={index} className={`leaderboard-item ${index < 3 ? 'top-three' : ''}`}>
                    <div className="rank-icon">
                        <span className={`rank ${index === 0 ? 'rank-1' : index === 1 ? 'rank-2' : index === 2 ? 'rank-3' : ''}`}>
                            {index + 1}
                        </span>
                    </div>
                    <span className="player-name">{player.userName}</span>
                    <span className="player-score">{player.elo}</span>
                </li>
                
                

                ))}
            </ul>
        </div>
    );
};

export default Leaderboard;
