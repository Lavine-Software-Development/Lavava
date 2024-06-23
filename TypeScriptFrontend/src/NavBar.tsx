import { NavLink } from "react-router-dom";
import "../styles/style.css";
import React, { useRef, useState } from "react";

export function NavBar() {
    const [open, setOpen] = useState<boolean>(false);
    const dropdrownRef = useRef<HTMLDivElement>(null);
    const handleDropDownFocus = (state: boolean) => {
        setOpen(!state);
    };
    const handleClickOutsideDropdown = (e: any) => {
        if (open && !dropdrownRef.current?.contains(e.target as Node)) {
            setOpen(false);
        }
    };
    window.addEventListener("click", handleClickOutsideDropdown);

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
                    src=""
                    width="50"
                    height="50"
                    alt=""
                    className="navLinkImage"
                />
                <h4 className="navLinkText">Lavava</h4>
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
