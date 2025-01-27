import React from "react";
import { Link } from "react-router-dom";

const LockedPage = () => {
  return (
    <div className="flex flex-col items-center p-8">
      <h1> You must be logged in to view this page. </h1>
      <Link className="font-bold" to="/profile">
        Go to login.
      </Link>
    </div>
  );
};

export default LockedPage;
