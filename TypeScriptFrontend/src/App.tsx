import { useRef, useState, useContext } from "react";
import React from "react";

import { IRefPhaserGame, PhaserGame } from "./game/PhaserGame";
import { MainMenu } from "./game/scenes/MainMenu";
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
import board_data from "./game/data/board_data.json";
import Register from "./user-flow/Register";
import ForgotPassword from "./user-flow/reset_password";
import Home from "./user-flow/Home";
import Profile from "./user-flow/Profile";
import DeckBuilder from "./user-flow/deck_builder";
import Lobby from "./user-flow/lobby";
import { NetworkContext, NetworkProvider } from "./game/NetworkContext";
import { use } from "matter";
function App() {
    const phaserRef = useRef<IRefPhaserGame | null>(null);

    // Event emitted from the PhaserGame component
    const currentScene = (scene: Phaser.Scene) => {};
    return (
        <Router>
            <NetworkProvider>
                <div
                    id="app"
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
                                        props={board_data}
                                        // network={network}
                                    />
                                </div>
                            }
                        />
                        <Route
                            path="/websocket-test"
                            element={<WebSocketTest />}
                        />
                        <Route
                            path="/"
                            element={<Navigate replace to="/login" />}
                        />
                        <Route path="/login" element={<Login />} />
                        <Route path="/register" element={<Register />} />
                        <Route
                            path="/forgot-password"
                            element={<ForgotPassword />}
                        />
                        <Route path="/home" element={<Home />} />
                        <Route path="/builder" element={<DeckBuilder />} />
                        <Route path="/profile" element={<Profile />} />
                        <Route path="/lobby" element={<Lobby />} />
                    </Routes>
                </div>
            </NetworkProvider>
        </Router>
    );
}

export default App;

