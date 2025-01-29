import React, { useState, useEffect, useRef } from "react";
import ModifyAccount from "./ModifyAccount";

const ManageAccounts = () => {
  const [accounts, setAccounts] = useState([]);
  const usernameInput = useRef();
  const passwordInput = useRef();

  const handleGetAccounts = async () => {
    try {
      const response = await fetch(`http://localhost:8080/accounts`);

      if (response.ok) {
        const data = await response.json();
        console.log(data);
        setAccounts(data);
      } else {
        setAccounts([]);
        console.error("No accounts found.");
      }
    } catch (error) {
      console.error("Error fetching accounts:", error);
    }
  };

  const handleCreateAccount = async () => {
    try {
      const response = await fetch("http://localhost:8080/accounts", {
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
        alert("Account created successfully!");
        handleGetAccounts();
      } else {
        console.error("Username already exists.");
      }
    } catch (error) {
      console.error("Error creating account:", error);
    }
  };

  useEffect(() => {
    handleGetAccounts();
  }, []);

  return (
    <>
      <div className="flex flex-col items-center p-8">
        <h2 className="text-xl font-bold"> Create Account </h2>
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
          onClick={handleCreateAccount}
        >
          Enter
        </button>
      </div>

      <h2 className="text-xl font-bold"> Modify Accounts </h2>
      {accounts.map((account, index) => (
        <ModifyAccount
          key={index}
          username={account.username}
          handleGetAccounts={handleGetAccounts}
        />
      ))}
    </>
  );
};

export default ManageAccounts;
