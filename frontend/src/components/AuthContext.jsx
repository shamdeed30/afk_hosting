import React, { useState, createContext, useContext } from "react";

const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [loggedIn, setLoggedIn] = useState(false);
  const [username, setUsername] = useState("");
  const [isAdmin, setIsAdmin] = useState(false);

  const login = async (username, password) => {
    try {
      const response = await fetch("http://localhost:8080/login", {
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
        const data = await response.json();
        setLoggedIn(true);
        setUsername(data[0]["username"]);
        if (data[0]["isAdmin"]) {
          setIsAdmin(true);
        }
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
    setIsAdmin(false);
  };

  return (
    <AuthContext.Provider
      value={{ username, loggedIn, isAdmin, login, logout }}
    >
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  return useContext(AuthContext);
};
