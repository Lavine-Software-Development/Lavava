import React, { useEffect, useState } from 'react';
import config from '../env-config';
import { useNavigate } from 'react-router-dom';

const HostSettings: React.FC = () => {
    const [totalNodes, setTotalNodes] = useState(0);
    const [totalEdges, setTotalEdges] = useState(0);
    const [portPercentage, setPortPercentage] = useState(0);
    const [startingMainlandCapitals, setStartingMainlandCapitals] = useState(0);
    const [startingIslandCapitals, setStartingIslandCapitals] = useState(0);
    const [startingCannons, setStartingCannons] = useState(0);
    const [startingPumps, setStartingPumps] = useState(0);
    const [twoWayPercentage, setTwoWayPercentage] = useState(0);

    const navigate = useNavigate();

    const handleStartFresh = () => {
    };

    const handleSaveSettings = () => {
        // Implement your save logic here
        // This could involve updating state, sending a request to a backend, etc.
        console.log("Settings saved");
    };

    const handleMySettings = () => {
    };

    const goHome = () => {
        navigate('/home');
    }

    useEffect(() => {
        fetch(`${config.userBackend}/default-host-settings`)
            .then((response) => response.json())
            .then((data) => {
                setTotalNodes(data.totalNodes);
                setTotalEdges(data.totalEdges);
                setPortPercentage(data.portPercentage);
                setStartingMainlandCapitals(data.startingMainlandCapitals);
                setStartingIslandCapitals(data.startingIslandCapitals);
                setStartingCannons(data.startingCannons);
                setStartingPumps(data.startingPumps);
                setTwoWayPercentage(data.twoWayPercentage);
            })
            .catch((error) => {
                console.error('Error:', error);
            });
        }, []);

    return (
        <div className="profile-card">
          <h2>Settings</h2>
          <div className="settings-card">
            <div className="column">
              <div className="row">
                <label>Total Nodes<input type="number" value={totalNodes} onChange={(e) => setTotalNodes(parseInt(e.target.value))} /></label>
              </div>
              <div className="row">
                <label>Total Edges<input type="number" value={totalEdges} onChange={(e) => setTotalEdges(parseInt(e.target.value))} /></label>
              </div>
              <div className="row">
                <label>Port Percentage<input type="number" value={portPercentage} onChange={(e) => setPortPercentage(parseInt(e.target.value))} /></label>
              </div>
              <div className="row">
                <label>Starting Mainland Capitals<input type="number" value={startingMainlandCapitals} onChange={(e) => setStartingMainlandCapitals(parseInt(e.target.value))} /></label>
              </div>
            </div>
            <div className="column">
              <div className="row">
                <label>Starting Island Capitals<input type="number" value={startingIslandCapitals} onChange={(e) => setStartingIslandCapitals(parseInt(e.target.value))} /></label>
              </div>
              <div className="row">
                <label>Starting Cannons<input type="number" value={startingCannons} onChange={(e) => setStartingCannons(parseInt(e.target.value))} /></label>
              </div>
              <div className="row">
                <label>Starting Pumps<input type="number" value={startingPumps} onChange={(e) => setStartingPumps(parseInt(e.target.value))} /></label>
              </div>
              <div className="row">
                <label>Two-Way Percentage<input type="number" value={twoWayPercentage} onChange={(e) => setTwoWayPercentage(parseInt(e.target.value))} /></label>
              </div>
            </div>
          </div>
          <div className="button-container">
            <div className="button-row">
                <button className="custom-button start-fresh-button" data-tooltip="Reset current settings" onClick={handleStartFresh}>Start Fresh</button>
                {localStorage.getItem('userToken') && (
                    <>
                        <button className="custom-button save-button" data-tooltip="Update your default settings" onClick={handleSaveSettings}>Save</button>
                        <button className="custom-button my-deck-button" data-tooltip="Use your default settings" onClick={handleMySettings}>My Settings</button>
                    </>
                )}
            </div>
                <button className="custom-button ready-button" data-tooltip="Go to the home page" onClick={goHome}>Ready</button>
            </div>
        </div>
      );
    };

export default HostSettings;