import { NavLink } from "react-router-dom";
import "../styles/style.css";
import React, { useRef, useState } from "react";

export function NavBar() {

    return (
        <nav className="navbar fixed-top">
            <NavLink to="/leaderboard" className="navLinkContainer">
                <img
                    src="./images/leaderboard logo.png"
                    width="60"
                    height="50"
                    alt=""
                    className="navLinkImage"
                />
                <h4 className="navLinkText">Leaderboard</h4>
            </NavLink>
            <NavLink to="/home" className="navLinkContainer">
                <img
                    src="./images/Home_orange.png"
                    width="50"
                    height="50"
                    alt=""
                    className="navLinkImage"
                />
                <h4 className="navLinkText">Durb</h4>
            </NavLink>
            <NavLink to="/profile" className="navLinkContainer">
                <img
                    src="./images/profile icon.png"
                    width="50"
                    height="50"
                    alt=""
                    className="navLinkImage"
                />
                <h4 className="navLinkText">Profile</h4>
            </NavLink>
        </nav>
    );
}
