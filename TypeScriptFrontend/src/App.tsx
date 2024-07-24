import { useRef, useState, useContext } from "react";
import React from "react";

import { IRefPhaserGame, PhaserGame } from "./game/PhaserGame";
import { useEffect } from "react";
import {
    BrowserRouter as Router,
    Routes,
    Route,
    Link,
    Navigate,
} from "react-router-dom";
import WebSocketTest from "./websocketClient"; // Import your WebSocketTest component if not already done
import Login from "./user-flow/login";
import Register from "./user-flow/Register";
import ForgotPassword from "./user-flow/reset_password";
import Home from "./user-flow/Home";
import Profile from "./user-flow/Profile";
import Team from './user-flow/team';
import DeckBuilder from "./user-flow/deck_builder";
import { NavBar } from "./NavBar";
import Leaderboard from "./user-flow/Leaderboard";
import HowToPlay from "./user-flow/How_to_play";
import ChangePassword from "./user-flow/change_password";
import Lobby from "./user-flow/lobby";
import { NetworkContext, NetworkProvider } from "./game/NetworkContext";
import { use } from "matter";
import HostSettings from "./user-flow/host_settings";

function App() {
    const phaserRef = useRef<IRefPhaserGame | null>(null);

    // Event emitted from the PhaserGame component
    const currentScene = (scene: Phaser.Scene) => {};
    return (
        <Router>
            <NetworkProvider>
                <div
                    style={{
                        fontFamily: "Arial, sans-serif",
                        lineHeight: "1.6",
                    }}
                >
                    <Routes>
                        <Route
                            path="/play"
                            element={
                                <div>
                                    <PhaserGame
                                        ref={phaserRef}
                                        currentActiveScene={currentScene}
                                    />
                                </div>
                            }
                        />
                        <Route path="/lobby" element={<Lobby />} />
                        <Route
                            path="*"
                            element={
                                <div id="app">
                                    <NavBar />
                                    <Routes>
                                        <Route path="/websocket-test" element={<WebSocketTest />} />
                                        <Route path="/" element={<Navigate replace to="/login" />} />
                                        <Route path="/login" element={<Login />} />
                                        <Route path="/register" element={<Register />} />
                                        <Route path="/forgot-password" element={<ForgotPassword />} />
                                        <Route path="/home" element={<Home />} />
                                        <Route path="/builder" element={<DeckBuilder />} />
                                        <Route path="/profile" element={<Profile />} />
                                        <Route path="/leaderboard" element={<Leaderboard />} />
                                        <Route path="/how-to-play" element={<HowToPlay />} />
                                        <Route path="/team" element={<Team />} />
                                        <Route path="/change-password" element={<ChangePassword />} />
                                        <Route path="/host-settings" element={<HostSettings />} />
                                    </Routes>
                                </div>
                            }
                        />
                    </Routes>
                </div>
            </NetworkProvider>
        </Router>
    );
}

export default App;

