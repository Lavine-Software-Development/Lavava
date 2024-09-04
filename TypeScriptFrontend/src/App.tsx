import React, { useRef, useState, useContext, useEffect } from "react";
import {
    createBrowserRouter,
    createRoutesFromElements,
    Route,
    Navigate,
    RouterProvider,
    Outlet,
    useLocation,
} from "react-router-dom";
import { IRefPhaserGame, PhaserGame } from "./game/PhaserGame";
import WebSocketTest from "./websocketClient";
import Login from "./user-flow/login";
import Register from "./user-flow/Register";
import ForgotPassword from "./user-flow/reset_password";
import Home from "./user-flow/Home";
import Profile from "./user-flow/Profile";
import Team from "./user-flow/team";
import DeckBuilder from "./user-flow/deck_builder";
import { NavBar } from "./NavBar";
import Leaderboard from "./user-flow/Leaderboard";
import HowToPlay from "./user-flow/How_to_play";
import ChangePassword from "./user-flow/change_password";
import Lobby from "./user-flow/lobby";
import MatchHistory from "./user-flow/MatchHistory";
import { NetworkProvider } from "./game/NetworkContext";
import Chatbot from "./user-flow/chatbot";

const router = createBrowserRouter(
    createRoutesFromElements(
        <Route path="/" element={<MainLayout />}>
            <Route index element={<Navigate replace to="/login" />} />
            <Route path="play" element={<PhaserGameWrapper />} />
            <Route path="lobby" element={<Lobby />} />
            <Route path="websocket-test" element={<WebSocketTest />} />
            <Route path="login" element={<Login />} />
            <Route path="register" element={<Register />} />
            <Route path="forgot-password" element={<ForgotPassword />} />
            <Route path="home" element={<Home />} />
            <Route path="builder" element={<DeckBuilder />} />
            <Route path="profile" element={<Profile />} />
            <Route path="leaderboard" element={<Leaderboard />} />
            <Route path="how-to-play" element={<HowToPlay />} />
            <Route path="team" element={<Team />} />
            <Route path="change-password" element={<ChangePassword />} />
            <Route path="match-history" element={<MatchHistory />} />
            <Route path="*" element={<Navigate replace to="/login" />} />
        </Route>
    )
);

function MainLayout() {
    const location = useLocation();
    const hideNavBar =
        location.pathname === "/play" || location.pathname === "/lobby";
    const hideChatbot = location.pathname === "/play";
    if (hideNavBar) {
        return <Outlet />;
    } else {
        return (
            <div id="app">
                <NavBar />
                <Outlet />
                <Chatbot />
            </div>
        );
    }
}
function PhaserGameWrapper() {
    const phaserRef = useRef<IRefPhaserGame | null>(null);
    const currentScene = (scene: Phaser.Scene) => {};

    return <PhaserGame ref={phaserRef} currentActiveScene={currentScene} />;
}

export default function App() {
    return (
        <NetworkProvider>
            <RouterProvider router={router} />
        </NetworkProvider>
    );
}

