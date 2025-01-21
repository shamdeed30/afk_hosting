import React from "react";
import GameCard from "./GameCard";

const Recent = () => {
  return (
    <div className="w-3/4 py-8">
      <div className="flex justify-between">
        <h2 className="py-8 text-3xl"> Recent </h2>
        <select className="py-8">
          <option value="week1"> Week 1 </option>
          <option value="week1"> Week 2 </option>
        </select>
      </div>

      <GameCard />
    </div>
  );
};

export default Recent;
