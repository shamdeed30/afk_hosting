import React, { useState, useRef } from "react";
// i think may have to use useContext to lock other pages based on if they're logged in

const ProfilePage = () => {
  const [loggedIn, setLoggedIn] = useState(false);
  const usernameInput = useRef();
  const passwordInput = useRef();

  const handleLogin = async () => {
    console.log(usernameInput.current.value);
    console.log(passwordInput.current.value);
    try {
      const response = await fetch("http://localhost:8080/login", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          username: usernameInput.current.value,
          password: passwordInput.current.value,
        }),
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
