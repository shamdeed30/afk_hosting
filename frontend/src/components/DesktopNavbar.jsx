import React from "react";
import { Link } from "react-router-dom";

const DesktopNavbar = () => {
  return (
    <nav className="sticky top-0 flex h-full justify-between border-b bg-white p-8">
      <Link className="font-kufam text-4xl font-extrabold" to="/">
        AFK
      </Link>
      <Link to="/ranking"> Ranking </Link>
      <Link to="/upload"> Upload </Link>
      <Link to="/modify"> Modify </Link>
      <Link to="/profile"> Profile </Link>
    </nav>
  );
};

export default DesktopNavbar;
