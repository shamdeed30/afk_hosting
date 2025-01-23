import React from "react";
import { Link } from "react-router-dom";
import { CgProfile } from "react-icons/cg";

const DesktopNavbar = () => {
  return (
    <nav className="sticky top-0 flex h-full justify-between border-b bg-white p-8">
      <Link className="font-kufam text-4xl font-extrabold" to="/">
        AFK
      </Link>
      <Link className="font-bold" to="/ranking">
        Ranking
      </Link>
      <Link className="font-bold" to="/upload">
        Upload
      </Link>
      <Link className="font-bold" to="/modify">
        Modify
      </Link>
      <Link className="font-bold" to="/profile">
        <CgProfile className="h-auto w-8" />
      </Link>
    </nav>
  );
};

export default DesktopNavbar;
