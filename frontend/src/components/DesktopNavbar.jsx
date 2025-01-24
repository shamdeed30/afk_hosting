import React from "react";
import { Link } from "react-router-dom";
import { CgProfile } from "react-icons/cg";

const DesktopNavbar = () => {
  return (
    <nav className="sticky top-0 flex h-full justify-between bg-zinc-900 p-8">
      <Link className="font-kufam text-4xl font-extrabold text-white" to="/">
        AFK
      </Link>
      <Link className="font-bold text-white" to="/ranking">
        Ranking
      </Link>
      <Link className="font-bold text-white" to="/upload">
        Upload
      </Link>
      <Link className="font-bold text-white" to="/modify">
        Modify
      </Link>
      <Link className="font-bold text-white" to="/profile">
        <CgProfile className="h-auto w-8" />
      </Link>
    </nav>
  );
};

export default DesktopNavbar;
