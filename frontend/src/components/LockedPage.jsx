import React from "react";
import { Link } from "react-router-dom";
import { MdLock } from "react-icons/md";

const LockedPage = () => {
  return (
    <div className="bg-custom-gray flex min-h-dvh flex-col items-center p-40 text-center text-white">
      <MdLock className="h-auto w-12" />
      <h1 className="p-8 text-3xl font-semibold">
        You must be logged in
        <br />
        to view this page.
      </h1>
      <Link
        className="bg-custom-off-white hover:bg-custom-gold px-8 py-2 font-bold text-black transition duration-300"
        to="/profile"
      >
        Go to Login
      </Link>
    </div>
  );
};

export default LockedPage;
