import React, { useRef } from "react";

const ModifyAccount = (props) => {
  const { username, handleGetAccounts } = props;
  const passwordChangeInput = useRef();

  const handleChangePassword = async (password) => {
    try {
      const response = await fetch("http://localhost:8080/accounts", {
        method: "PUT",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          username: username,
          password: passwordChangeInput.current.value,
        }),
      });

      if (response.ok) {
        alert("Password updated successfully!");
      } else {
        console.error("Account not found.");
      }
    } catch (error) {
      console.error("Error updating password:", error);
    }
  };

  const handleDeleteAccount = async () => {
    try {
      const response = await fetch("http://localhost:8080/accounts", {
        method: "DELETE",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          username: username,
        }),
      });

      if (response.ok) {
        alert("Account deleted successfully!");
        handleGetAccounts();
      } else {
        console.error("Account not found.");
      }
    } catch (error) {
      console.error("Error deleting account:", error);
    }
  };

  return (
    <div className="flex items-center justify-center border-b p-4">
      <h3 className="p-4 font-bold">{username}</h3>
      <div className="p-4">
        <input
          type="password"
          placeholder="New Password"
          ref={passwordChangeInput}
          className="rounded-lg border p-2"
        />
        <button
          onClick={handleChangePassword}
          className="rounded-lg border bg-blue-500 p-2 text-white"
        >
          Change Password
        </button>
      </div>

      <button
        onClick={handleDeleteAccount}
        className="rounded-lg border bg-red-500 p-2 text-white"
      >
        Delete Account
      </button>
    </div>
  );
};

export default ModifyAccount;
