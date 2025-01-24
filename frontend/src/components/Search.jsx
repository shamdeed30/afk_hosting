import React, { useState, useEffect } from "react";
import GameCard from "./GameCard";

const Search = () => {
  const [game, setGame] = useState("RL");
  const [week, setWeek] = useState("1");
  const [gameReports, setGameReports] = useState([]);

  const handleGameChange = (event) => {
    setGame(event.target.value);
  };

  const handleWeekChange = (event) => {
    setWeek(event.target.value);
  };

  // Function to fetch game reports from the backend
  const getGameReports = async () => {
    try {
      const response = await fetch(
        `http://40.85.147.30:8080/stats/${game}/${week}`,
      );

      if (response.ok) {
        const data = await response.json();
        setGameReports(data);
      } else {
        setGameReports([]);
        console.error("No data found");
      }
    } catch (error) {
      console.error("Error fetching game stats:", error);
    }
  };

  // update stats when filters get changed
  useEffect(() => {
    getGameReports();
  }, [game, week]);

  useEffect(() => {
    console.log(gameReports);
  }, [gameReports]);

  return (
    <div className="w-3/4 py-8">
      {/* Page title */}
      <h2 className="py-8 text-3xl"> Search </h2>

      {/* Dropdowns for selecting game and week */}
      <div className="flex">
        <select
          className="border-black-300 rounded-lg border py-8"
          onChange={handleGameChange}
          value={game}
        >
          <option value="RL">Rocket League</option>
          <option value="Val">Valorant</option>
          <option value="Apex">Apex Legends</option>
        </select>

        <select
          className="mx-8 rounded-lg border border-gray-300 py-8"
          onChange={handleWeekChange}
          value={week}
        >
          <option value="1">Week 1</option>
          <option value="2">Week 2</option>
          <option value="3">Week 3</option>
          <option value="4">Week 4</option>
          <option value="5">Week 5</option>
          <option value="6">Week 6</option>
          <option value="7">Season Averages</option>
        </select>

        {/* Input for player search (currently not connected to backend) */}
        <input
          type="text"
          placeholder="Find a player's stats by name"
          className="w-full border border-black p-4"
        />
      </div>

      {/* Render game reports dynamically */}
      <div className="py-8">
        {gameReports.map((gameReport, index) => (
          <GameCard
            key={index} // Unique game key for each report
            match={gameReport.match} // Match information
            teamStats={gameReport.teamStats} // Team stats
            opponentStats={gameReport.opponentStats} // Opponent stats
          />
        ))}
      </div>
    </div>
  );
};

export default Search;