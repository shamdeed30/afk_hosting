import React from "react";
import SearchBar from "./SearchBar";
import Recent from "./Recent";

const HomePage = () => {
  return (
    <div className="flex h-max w-full flex-col items-center">
      <h1 className="p-12 text-4xl font-bold"> SCAC Esports Tracker</h1>
      <SearchBar />
      <Recent />
    </div>
  );
};

export default HomePage;
