import { useRef, useState } from "react";
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
import { Main } from "./game/objects/parse";
import board_data from "./game/data/board_data.json";
import { BoardJSON } from "./game/objects/parse";
import Register from "./user-flow/Register";
import ForgotPassword from "./user-flow/reset_password";
import Home from "./user-flow/Home";
import Profile from "./user-flow/Profile";
import DeckBuilder from "./user-flow/deck_builder";
function App() {
    const phaserRef = useRef<IRefPhaserGame | null>(null);

    const testMain = () => {
        const main = new Main();
        console.log("test");
        console.log(typeof board_data);
        main.setup(board_data as BoardJSON);
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
                    <Route path="/websocket-test" element={<WebSocketTest />} />
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
                </Routes>
            </div>
        </Router>
    );
}

export default App;

