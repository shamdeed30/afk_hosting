import React from "react";

const SearchBar = () => {
  return (
    <div className="w-3/4 py-8">
      <h2 className="py-8 text-3xl"> Search </h2>
      <input
        type="text"
        placeholder="Search"
        className="w-full border border-black p-4"
      />
    </div>
  );
};

export default SearchBar;
