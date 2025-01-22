import React, { useState } from "react";

const RankingPage = () => {
  const [selectedGame, setSelectedGame] = useState("Rocket League");

  const handleGameChange = (event) => {
    setSelectedGame(event.target.value);
  };

  return (
    <div className="flex min-h-screen flex-col items-center justify-center bg-gray-100 p-6">
      <h1 className="mb-8 text-4xl font-bold">Game Rankings</h1>

      {/* Dropdown Menu */}
      <select
        className="mb-8 rounded-lg border border-gray-300 p-4"
        value={selectedGame}
        onChange={handleGameChange}
      >
        <option value="Rocket League">Rocket League</option>
        <option value="Valorant">Valorant</option>
        <option value="Apex Legends">Apex Legends</option>
      </select>

      {/* Display Table Based on Selected Game */}
      {selectedGame === "Rocket League" || selectedGame === "Valorant" ? (
        <RLAndValTable />
      ) : (
        <ApexTable />
      )}
    </div>
  );
};

// Demo data for Rocket League and Valorant
const RLAndValTable = () => {
  return (
    <div className="w-3/4">
      <table className="w-full table-auto border border-gray-300 text-left">
        <thead className="bg-gray-200">
          <tr>
            <th className="px-4 py-4">School</th>
            <th className="px-4 py-4">Wins</th>
            <th className="px-4 py-4">Losses</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td className="px-4 py-4">Colorado College</td>
            <td className="px-4 py-4">5</td>
            <td className="px-4 py-4">3</td>
          </tr>
          <tr>
            <td className="px-4 py-4">School B</td>
            <td className="px-4 py-4">6</td>
            <td className="px-4 py-4">2</td>
          </tr>
        </tbody>
      </table>
    </div>
  );
};

// Demo data for Apex Legends
const ApexTable = () => {
  return (
    <div className="w-3/4">
      <table className="w-full table-auto border border-gray-300 text-left">
        <thead className="bg-gray-200">
          <tr>
            <th className="px-4 py-4">School</th>
            <th className="px-4 py-4">Week</th>
            <th className="px-4 py-4">1st</th>
            <th className="px-4 py-4">2nd</th>
            <th className="px-4 py-4">3rd</th>
            <th className="px-4 py-4">4th</th>
            <th className="px-4 py-4">Kills</th>
            <th className="px-4 py-4">Damage</th>
            <th className="px-4 py-4">Total Points</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td className="px-4 py-4">Colorado College</td>
            <td className="px-4 py-4">1</td>
            <td className="px-4 py-4">1</td>
            <td className="px-4 py-4">0</td>
            <td className="px-4 py-4">2</td>
            <td className="px-4 py-4">1</td>
            <td className="px-4 py-4">15</td>
            <td className="px-4 py-4">1200</td>
            <td className="px-4 py-4">
              {12 + 0 + 14 + 5 + 15 + Math.floor(1200 / 200)}
            </td>
          </tr>
          <tr>
            <td className="px-4 py-4">School B</td>
            <td className="px-4 py-4">1</td>
            <td className="px-4 py-4">0</td>
            <td className="px-4 py-4">1</td>
            <td className="px-4 py-4">0</td>
            <td className="px-4 py-4">0</td>
            <td className="px-4 py-4">10</td>
            <td className="px-4 py-4">800</td>
            <td className="px-4 py-4">
              {9 + 0 + 0 + 0 + 10 + Math.floor(800 / 200)}
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  );
};

export default RankingPage;
