import React, { useState, useEffect, useRef } from "react";
import GameCard from "./GameCard";
import PlayerReport from "./PlayerReport";
import { IoSearch } from "react-icons/io5";

const HomePage = () => {
  const [game, setGame] = useState("RL");
  const [week, setWeek] = useState("1");
  const [gameReports, setGameReports] = useState([]);
  const [playerReports, setPlayerReports] = useState([]);
  const searchInput = useRef();

  const handleGameChange = (event) => {
    setGame(event.target.value);
  };

  const handleWeekChange = (event) => {
    setWeek(event.target.value);
  };

  const handleGetPlayerReports = async () => {
    try {
      const response = await fetch(
        `http://localhost:8080/player/${game}?player=${encodeURIComponent(searchInput.current.value)}`,
      );

      if (response.ok) {
        const data = await response.json();
        setPlayerReports(data);
      } else {
        console.error("Couldn't find any stats for this player.");
        setPlayerReports([]);
      }
    } catch (error) {
      console.error("Error fetching the player stats:", error);
    }
  };

  const handleGetGameReports = async () => {
    try {
      const response = await fetch(
        `http://localhost:8080/stats/${game}/${week}`,
      );

      if (response.ok) {
        const data = await response.json();
        setGameReports(data);
      } else {
        setGameReports([]);
        console.error("No stats found.");
      }
    } catch (error) {
      console.error("Error fetching game stats:", error);
    }
  };

  // update stats when filters get changed
  useEffect(() => {
    handleGetGameReports();
    handleGetPlayerReports();
  }, [game, week]);

  return (
    <div
      className={`${
        game === "Val"
          ? "bg-custom-Val"
          : game === "RL"
            ? "bg-custom-RL"
            : "bg-custom-Apex"
      } relative flex min-h-dvh justify-center p-8`}
    >
      <div
        className={`${
          game === "Val"
            ? "bg-[url(./media/Valorant.jpeg)]"
            : game === "RL"
              ? "bg-[url(./media/Rocket_League.jpeg)]"
              : "bg-[url(./media/Apex_Legends.jpeg)]"
        } absolute left-0 top-0 z-0 h-full w-full bg-cover bg-center opacity-40`}
      ></div>

      <div className="relative z-10 flex w-3/4 flex-col items-center">
        <div className="w-full py-16 text-white">
          <h1 className="py-8 text-3xl font-semibold"> Search </h1>

          <div className="flex rounded-md bg-custom-gray p-4">
            <select
              className="mx-2 rounded-md border border-custom-off-white bg-custom-gray py-8"
              onChange={handleGameChange}
              value={game}
            >
              <option value="RL">Rocket League</option>
              <option value="Val">Valorant</option>
              <option value="Apex">Apex Legends</option>
            </select>

            <select
              className="mx-2 rounded-md border border-custom-off-white bg-custom-gray py-8"
              onChange={handleWeekChange}
              value={week}
            >
              <option value="1">Week 1</option>
              <option value="2">Week 2</option>
              <option value="3">Week 3</option>
              <option value="4">Week 4</option>
              <option value="5">Week 5</option>
              <option value="6">Week 6</option>
              <option value="7">Averages</option>
            </select>

            <div className="relative w-full">
              <input
                type="text"
                placeholder="Find a player's stats by name"
                className="h-full w-full rounded-md border border-black p-4"
                ref={searchInput}
              />
              <IoSearch
                className="absolute right-4 top-5 h-auto w-12"
                onClick={handleGetPlayerReports}
              />
            </div>
          </div>
        </div>

        {playerReports.length > 0 ? (
          <div className="w-full">
            <h2 className="py-8 text-2xl font-semibold">Player Stats</h2>
            {/* Renders player reports dynamically */}
            <div className="z-30 w-full rounded-md bg-custom-gray">
              <PlayerReport
                player={searchInput.current.value}
                playerReports={playerReports}
              />
            </div>
          </div>
        ) : null}

        <div className="w-full">
          <h2 className="py-8 text-2xl font-semibold">Game Stats</h2>
          {/* Renders game reports dynamically */}
          <div className="z-30 w-full rounded-md bg-custom-gray">
            {gameReports.length > 0 ? (
              gameReports.map((gameReport, index) => (
                <GameCard
                  key={index} // Unique game key for each report
                  match={gameReport.match} // Match information
                  teamStats={gameReport.teamStats} // Team stats
                  opponentStats={gameReport.opponentStats} // Opponent stats
                />
              ))
            ) : (
              <h3 className="p-12 text-center text-xl font-bold">
                Nothing to see here...
              </h3>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default HomePage;
