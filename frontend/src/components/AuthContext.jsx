import React, { useState, createContext, useContext } from "react";

const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [loggedIn, setLoggedIn] = useState(true);
  const [username, setUsername] = useState("");

  const login = async (username, password) => {
    try {
      const response = await fetch("http://40.85.147.30:8080/login", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          username: username,
          password: password,
        }),
      });

      if (response.ok) {
        setLoggedIn(true);
        setUsername(username);
      } else {
        console.log();
      }
    } catch (error) {
      console.error("Invalid credentials.", error);
    }
  };

  const logout = () => {
    setLoggedIn(false);
    setUsername("");
  };

  return (
    <AuthContext.Provider value={{ username, loggedIn, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  return useContext(AuthContext);
};
