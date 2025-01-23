import React from "react";
import Search from "./Search";

const HomePage = () => {
  return (
    <div className="flex h-max w-full flex-col items-center">
      <h1 className="p-12 text-4xl font-bold"> SCAC Esports Stats </h1>
      <Search />
    </div>
  );
};

export default HomePage;
