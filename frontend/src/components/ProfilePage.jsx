import React, { useState } from "react";

const ProfilePage = () => {
  const [loggedIn, setLoggedIn] = useState(false);

  const handleLogin = async () => {
    try {
      const response = await fetch(`http://localhost:8080/profile/`, {
        method: "PUT",
      });

      if (response.ok) {
        setLoggedIn(true);
      } else {
        console.log();
      }
    } catch (error) {
      console.error("Invalid credentials.", error);
    }
  };

  return (
    <div className="flex justify-center">
      {loggedIn ? (
        <div>
          <h2> Username </h2>
          <p> Forgot Password </p>
        </div>
      ) : (
        <div className="flex flex-col items-center p-8">
          <h2 className="text-xl font-bold"> Login </h2>
          <input
            type="text"
            placeholder="Username"
            className="m-8 w-full border border-black p-4"
          ></input>
          <input
            type="password"
            placeholder="Password"
            className="m-8 w-full border border-black p-4"
          ></input>
          <button
            className="rounded-lg border bg-blue-500 p-4 text-white"
            onClick={handleLogin}
          >
            Enter
          </button>
        </div>
      )}
    </div>
  );
};

export default ProfilePage;
