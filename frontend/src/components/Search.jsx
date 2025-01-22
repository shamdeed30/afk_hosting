import React, { useState, useEffect } from "react";
import GameCard from "./GameCard";

// Example game report
// {
//   "match": {
//     "school": "Colorado College",
//     "opponent": "Trinity University",
//     "didWin": true,
//     "teamScore": 5,
//     "opponentScore": 3
//   },
//   "teamStats": [
//     {
//       "school": "Colorado College",
//       "playerName": "Sir James",
//       "score": 780,
//       "goals": 3,
//       "assists": 2,
//       "saves": 4,
//       "shots": 7
//     },
//     {
//       "school": "Colorado College",
//       "playerName": "Penguin",
//       "score": 620,
//       "goals": 1,
//       "assists": 1,
//       "saves": 3,
//       "shots": 5
//     },
//     {
//       "school": "Colorado College",
//       "player_name": "Pineapple",
//       "score": 540,
//       "goals": 1,
//       "assists": 0,
//       "saves": 2,
//       "shots": 4
//     }
//   ],
//   "opponentStats": [
//     {
//       "school": "Trinity University",
//       "playerName": "GiraffeMan",
//       "score": 700,
//       "goals": 2,
//       "assists": 1,
//       "saves": 2,
//       "shots": 6
//     },
//     {
//       "school": "Trinity University",
//       "playerName": "Dog lover",
//       "score": 500,
//       "goals": 1,
//       "assists": 0,
//       "saves": 3,
//       "shots": 5
//     },
//     {
//       "school": "Trinity University",
//       "playerName": "Cpt. Morgan",
//       "score": 450,
//       "goals": 0,
//       "assists": 2,
//       "saves": 1,
//       "shots": 3
//     }
//   ]
// }

const Search = () => {
  const [game, setGame] = useState("valorant");
  const [week, setWeek] = useState("week1");
  const [gameReports, setGameReports] = useState([
    {
      match: {
        school: "Colorado College",
        opponent: "Trinity University",
        didWin: true,
        teamScore: 5,
        opponentScore: 3,
      },
      teamStats: [
        {
          school: "Colorado College",
          playerName: "Sir James",
          score: 780,
          goals: 3,
          assists: 2,
          saves: 4,
          shots: 7,
        },
        {
          school: "Colorado College",
          playerName: "Penguin",
          score: 620,
          goals: 1,
          assists: 1,
          saves: 3,
          shots: 5,
        },
        {
          school: "Colorado College",
          player_name: "Pineapple",
          score: 540,
          goals: 1,
          assists: 0,
          saves: 2,
          shots: 4,
        },
      ],
      opponentStats: [
        {
          school: "Trinity University",
          playerName: "GiraffeMan",
          score: 700,
          goals: 2,
          assists: 1,
          saves: 2,
          shots: 6,
        },
        {
          school: "Trinity University",
          playerName: "Dog lover",
          score: 500,
          goals: 1,
          assists: 0,
          saves: 3,
          shots: 5,
        },
      ],
    },
    {
      match: {
        school: "Colorado College",
        opponent: "Trinity University",
        didWin: true,
        teamScore: 5,
        opponentScore: 3,
      },
      teamStats: [
        {
          school: "Colorado College",
          playerName: "Sir James",
          score: 780,
          goals: 3,
          assists: 2,
          saves: 4,
          shots: 7,
        },
        {
          school: "Colorado College",
          playerName: "Penguin",
          score: 620,
          goals: 1,
          assists: 1,
          saves: 3,
          shots: 5,
        },
        {
          school: "Colorado College",
          player_name: "Pineapple",
          score: 540,
          goals: 1,
          assists: 0,
          saves: 2,
          shots: 4,
        },
      ],
      opponentStats: [
        {
          school: "Trinity University",
          playerName: "GiraffeMan",
          score: 700,
          goals: 2,
          assists: 1,
          saves: 2,
          shots: 6,
        },
        {
          school: "Trinity University",
          playerName: "Dog lover",
          score: 500,
          goals: 1,
          assists: 0,
          saves: 3,
          shots: 5,
        },
        {
          school: "Trinity University",
          playerName: "Cpt. Morgan",
          score: 450,
          goals: 0,
          assists: 2,
          saves: 1,
          shots: 3,
        },
      ],
    },
  ]);

  const handleGameChange = (event) => {
    setGame(event.target.value);
  };

  const handleWeekChange = (event) => {
    setWeek(event.target.value);
  };

  // get request for game stats (expects a list of game objects)
  const getGameReports = async () => {
    try {
      const response = await fetch(
        `http://localhost:3000/stats/${game}/${week}`,
      );

      if (response.ok) {
        const data = await response.json();

        setGameReports([...gameReports, data]);
      }
    } catch (error) {
      throw new Error("Error getting game stats.");
    }
  };

  // update stats when filters get changed
  // useEffect(() => {
  //   getGameReports();
  // }, [game, week]);

  return (
    <div className="w-3/4 py-8">
      <h2 className="py-8 text-3xl"> Search </h2>

      <div className="flex">
        <select className="py-8" onChange={handleGameChange}>
          <option value="valorant">Valorant</option>
          <option value="apex-legends"> Apex Legends </option>
          <option value="rocket-league"> Rocket League </option>
        </select>
        <select className="mx-8 py-8" onChange={handleWeekChange}>
          <option value="week1"> Week 1 </option>
          <option value="week2"> Week 2 </option>
          <option value="week3"> Week 3 </option>
          <option value="week4"> Week 4 </option>
          <option value="week5"> Week 5 </option>
          <option value="week6"> Week 6 </option>
        </select>
        <input
          type="text"
          placeholder="Find a player's stats by name"
          className="w-full border border-black p-4"
        />
      </div>

      <div className="py-8">
        {gameReports.map((gameReport) => (
          <GameCard
            match={gameReport.match}
            teamStats={gameReport.teamStats}
            opponentStats={gameReport.opponentStats}
          />
        ))}
      </div>
    </div>
  );
};

export default Search;
