import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";

const SuperAdminPage = () => {
  const [matches, setMatches] = useState([
    {
      id: 1,
      school: "Colorado College",
      opponent: "School B",
      week: "Week 1",
      games: [
        {
          id: 101,
          gameType: "Valorant",
          map: "Ascent",
          verified: false,
        },
        {
          id: 102,
          gameType: "Rocket League",
          map: "Champions Field",
          verified: true,
        },
      ],
    },
    {
      id: 2,
      school: "School C",
      opponent: "School D",
      week: "Week 2",
      games: [
        {
          id: 103,
          gameType: "Apex Legends",
          code: "ACD123",
          verified: false,
        },
        {
          id: 104,
          gameType: "Valorant",
          map: "Bind",
          verified: false,
        },
      ],
    },
  ]);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();

  useEffect(() => {
    // Fetch all matches from backend
    const fetchMatches = async () => {
      try {
        const response = await fetch("http://127.0.0.1:8080/get_all_matches");
        const data = await response.json();
        setMatches(data);
        setLoading(false);
      } catch (error) {
        console.error("Error fetching matches:", error);
        setLoading(false);
      }
    };

    fetchMatches();
  }, []);

  // Function to verify a game
  const handleVerify = (matchId, gameId) => {
    navigate("/modify", { state: { matchId, gameId } });
  };

  // Function to delete a game (with confirmation)
  const handleDelete = async (matchId, gameId) => {
    const confirmDelete = window.confirm(
      "Are you sure you want to delete this game?",
    );
    if (!confirmDelete) return;

    try {
      const response = await fetch(
        `http://127.0.0.1:8080/delete_game/${matchId}/${gameId}`,
        {
          method: "DELETE",
        },
      );

      if (response.ok) {
        alert("Game deleted successfully!");
        setMatches((prevMatches) =>
          prevMatches.map((match) =>
            match.id === matchId
              ? {
                  ...match,
                  games: match.games.filter((game) => game.id !== gameId),
                }
              : match,
          ),
        );
      } else {
        alert("Failed to delete game.");
      }
    } catch (error) {
      console.error("Error deleting game:", error);
    }
  };

  // Function to submit (verify) a match
  const handleSubmitMatch = async (matchId) => {
    const match = matches.find((m) => m.id === matchId);
    const allVerified = match.games.every((game) => game.verified);

    if (!allVerified) {
      alert("All games must be verified before submitting.");
      return;
    }

    try {
      const response = await fetch(
        `http://127.0.0.1:8080/verify_match/${matchId}`,
        {
          method: "POST",
        },
      );

      if (response.ok) {
        alert("Match successfully verified and submitted!");
        setMatches((prevMatches) =>
          prevMatches.filter((match) => match.id !== matchId),
        );
      } else {
        alert("Failed to submit match.");
      }
    } catch (error) {
      console.error("Error submitting match:", error);
    }
  };

  if (loading) return <p>Loading matches...</p>;

  return (
    <div className="flex min-h-screen flex-col items-center bg-custom-blue p-8">
      <h1 className="mb-6 text-3xl font-bold text-white">
        Super Admin - Verify Matches
      </h1>

      {matches.map((match) => (
        <div
          key={match.id}
          className="mb-6 w-3/4 rounded-lg bg-custom-gray p-4 text-white"
        >
          <h2 className="text-xl font-semibold">
            {match.school} vs {match.opponent}
          </h2>
          <p className="text-custom-off-white">Week: {match.week}</p>

          {/* Games Table */}
          <table className="mt-4 w-full border-collapse">
            <thead>
              <tr className="border-b border-custom-off-white">
                <th className="p-2">Game</th>
                <th className="p-2">Status</th>
                <th className="p-2">Actions</th>
              </tr>
            </thead>
            <tbody>
              {match.games.map((game) => (
                <tr key={game.id} className="border-b border-custom-off-white">
                  <td className="p-2">
                    {game.gameType} ({game.map || game.code})
                  </td>
                  <td className="p-2">
                    {game.verified ? "✅ Verified" : "⏳ Pending"}
                  </td>
                  <td className="p-2">
                    {!game.verified && (
                      <button
                        className="rounded-md bg-green-500 px-4 py-2 text-white hover:bg-green-600"
                        onClick={() => handleVerify(match.id, game.id)}
                      >
                        Verify
                      </button>
                    )}
                    <button
                      className="ml-2 rounded-md bg-red-500 px-4 py-2 text-white hover:bg-red-600"
                      onClick={() => handleDelete(match.id, game.id)}
                    >
                      Delete
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>

          {/* Submit Match Button (enabled only when all games are verified) */}
          {match.games.every((game) => game.verified) && (
            <button
              className="mt-4 rounded-lg bg-blue-500 px-6 py-3 text-white hover:bg-blue-600"
              onClick={() => handleSubmitMatch(match.id)}
            >
              Submit Match
            </button>
          )}
        </div>
      ))}
    </div>
  );
};

export default SuperAdminPage;
