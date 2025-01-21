import React from "react";
import { Link } from "react-router-dom";

const DesktopNavbar = () => {
  return (
    <nav className="flex h-full justify-between bg-black text-white">
      <Link to="/"> AFK </Link>
      <Link to="/upload"> Upload </Link>
      <Link to="/modify"> Modify </Link>
      <Link to="/profile"> Profile </Link>
    </nav>
  );
};

export default DesktopNavbar;
