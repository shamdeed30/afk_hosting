import React, { useState } from "react";
import { Link } from "react-router-dom";
import { CgProfile } from "react-icons/cg";
import { useAuth } from "./AuthContext";
import { MdLock } from "react-icons/md";
import Hamburger from "hamburger-react";

const DesktopNavbar = () => {
  const [menu, setMenu] = useState(false);
  const { loggedIn } = useAuth();

  return (
    <nav className="bg-custom-dark-gray sticky top-0 z-50 flex h-[7rem] items-center justify-between">
      <Link
        className="font-racing text-custom-off-white hover:text-custom-gold p-4 px-8 text-4xl font-extrabold"
        to="/"
        onClick={() => setMenu(false)}
      >
        AFK
      </Link>

      <div className="flex items-center p-4">
        <Hamburger color="#D9D9D9" toggled={menu} toggle={setMenu} />
        <Link
          className="p-4 font-bold text-white"
          to="/profile"
          onClick={() => setMenu(false)}
        >
          <CgProfile className="text-custom-off-white h-auto w-8" />
        </Link>
      </div>

      {menu && (
        <div className="bg-custom-gray fixed left-0 top-[7rem] z-40 flex h-dvh w-full justify-center">
          <div className="flex flex-col items-center px-8 py-24">
            <h6> STATS </h6>
            <Link
              className="text-custom-off-white hover:text-custom-gold p-8 text-5xl"
              to="/"
              onClick={() => setMenu(false)}
            >
              Home
            </Link>
            <Link
              className="text-custom-off-white hover:text-custom-gold p-8 text-5xl"
              to="/rankings"
              onClick={() => setMenu(false)}
            >
              Rankings
            </Link>
          </div>
          <div className="border-custom-off-white flex flex-col items-center border-l px-8 py-24">
            <h6> CHANGE </h6>
            <div className="text-custom-off-white hover:text-custom-gold flex p-8">
              <Link
                className="pr-4 text-5xl"
                to="/upload"
                onClick={() => setMenu(false)}
              >
                Upload
              </Link>
              <MdLock className="h-auto w-12" />
            </div>

            <div className="text-custom-off-white hover:text-custom-gold flex p-8">
              <Link
                className="pr-4 text-5xl"
                to="/modify"
                onClick={() => setMenu(false)}
              >
                Modify
              </Link>
              <MdLock className="h-auto w-12" />
            </div>
          </div>
        </div>
      )}
    </nav>
  );
};

export default DesktopNavbar;
