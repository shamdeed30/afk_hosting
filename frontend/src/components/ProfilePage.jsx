import React, { useRef } from "react";
import { useAuth } from "./AuthContext";

const ProfilePage = () => {
  const usernameInput = useRef();
  const passwordInput = useRef();

  const { username, loggedIn, login, logout } = useAuth();

  const handleLogin = () => {
    login(usernameInput.current.value, passwordInput.current.value);
  };

  return (
    <div className="flex justify-center">
      {loggedIn ? (
        <div className="flex flex-col items-center p-8">
          <h2 className="p-8 text-2xl font-bold">Username:</h2>
          <h3 className="p-8 text-xl"> {username} </h3>
          <button
            className="rounded-lg border bg-blue-500 p-4 text-white"
            onClick={logout}
          >
            Logout
          </button>
          <a
            href="mailto:p_hour@coloradocollege.edu"
            className="text-xl text-black"
          >
            Forgot Password
          </a>
        </div>
      ) : (
        <div className="flex flex-col items-center p-8">
          <h2 className="text-xl font-bold"> Login </h2>
          <input
            type="text"
            placeholder="Username"
            ref={usernameInput}
            className="m-8 w-full border border-black p-4"
          ></input>
          <input
            type="text"
            placeholder="Password"
            ref={passwordInput}
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
