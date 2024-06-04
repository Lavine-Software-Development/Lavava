import { useRef, useState } from "react";
import React from "react";

import { IRefPhaserGame, PhaserGame } from "./game/PhaserGame";
import { MainMenu } from "./game/scenes/MainMenu";
import { useEffect } from "react";
import { BrowserRouter as Router, Routes, Route, Link } from "react-router-dom";
import WebSocketTest from "./websocketClient"; // Import your WebSocketTest component if not already done
import Login from './user-flow/login';
import { Main } from "./game/slav/Objects/parse";
import board_data from "./game/slav/Objects/board_data.json";
import Register from "./user-flow/Register";
import ForgotPassword from "./user-flow/reset_password";
import Home from "./user-flow/Home";
import Profile from "./user-flow/profile";
function App() {

    const phaserRef = useRef<IRefPhaserGame | null>(null);

    const testMain = () => {
        const main = new Main();
        console.log("test");
        console.log(typeof board_data);
        main.setup(board_data);
        const updates = { "97": { on: true } };
        console.log(main.parse(main.edges, updates));
    };

    // Event emitted from the PhaserGame component
    const currentScene = (scene: Phaser.Scene) => {};

    return (
        <Router>
            <div
                id="app"
                style={{ fontFamily: "Arial, sans-serif", lineHeight: "1.6" }}
            >
                <Routes>
                    <Route
                        path="/"
                        element={
                            <div>
                                <PhaserGame
                                    ref={phaserRef}
                                    currentActiveScene={currentScene}
                                />
                            </div>
                        }
                    />
                    <Route path="/websocket-test" element={<WebSocketTest />} />
                    <Route path="/login" element={<Login />} />
                    <Route path="/register" element={<Register />} />
                    <Route path="/forgot-password" element={<ForgotPassword />} />
                    <Route path="/home" element={<Home />} />
                    <Route path="/profile" element={<Profile />} />
                </Routes>
            </div>
        </Router>
    );
}

export default App;

