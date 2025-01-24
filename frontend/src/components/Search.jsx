import React, { useState, useEffect } from "react";
import GameCard from "./GameCard";

const Search = () => {
  const [game, setGame] = useState("valorant");
  const [week, setWeek] = useState("week1");
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
      // const response = await fetch(`http://127.0.0.1:5000/stats/${game}/${week}`);
      // Change the URL to the backend server URL when Flask is up and running
      const response = await fetch(
        `http://40.85.147.30/stats/${game}/${week}`,
      );

      if (response.ok) {
        const data = await response.json();
        setGameReports([data]);
      } else {
        console.error("No data found");
      }
    } catch (error) {
      console.error("Error fetching game stats:", error);
    }
  };

  // update stats when filters get changed
  // useEffect(() => {
  //   getGameReports();
  // }, [game, week]);

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
          <option value="valorant">Valorant</option>
          <option value="apex-legends">Apex Legends</option>
          <option value="rocket-league">Rocket League</option>
        </select>

        <select
          className="mx-8 rounded-lg border border-gray-300 py-8"
          onChange={handleWeekChange}
          value={week}
        >
          <option value="week1">Week 1</option>
          <option value="week2">Week 2</option>
          <option value="week3">Week 3</option>
          <option value="week4">Week 4</option>
          <option value="week5">Week 5</option>
          <option value="week6">Week 6</option>
          <option value="week6">Season Averages</option>
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
