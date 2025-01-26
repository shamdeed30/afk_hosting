import React, { useState } from "react";

const ModifyPage = () => {
  // Mock data for testing the form
  const mockData = {
    game: "rocket-league",
    week: "1",
    school: "Colorado College",
    opponent: "Stanford",
    players: [
      {
        school: "Colorado College",
        playerName: "Jimmy Andrews",
        score: 400,
        goals: 2,
        assists: 1,
        saves: 3,
        shots: 5,
      },
      {
        school: "Stanford",
        playerName: "Chris Taylor",
        score: 350,
        goals: 2,
        assists: 1,
        saves: 2,
        shots: 4,
      },
    ],
  };

  // Initialize state with mock data
  const [formData, setFormData] = useState(mockData);

  // Update handler for editable fields
  const handleInputChange = (event, index, key) => {
    const updatedPlayers = [...formData.players];
    updatedPlayers[index][key] = event.target.value;
    setFormData({ ...formData, players: updatedPlayers });
  };

  // Update handler for dropdowns (e.g., game, week)
  const handleDropdownChange = (event, key) => {
    setFormData({ ...formData, [key]: event.target.value });
  };

  const handleSubmit = () => {
    console.log("Verified and Submitted Data:", formData);
    alert("Data verified and submitted!");
    // TODO: Implement backend submission logic
  };

  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-gray-100 p-6">
      <h1 className="text-4xl font-bold mb-8">Modify Game Data</h1>

      {/* Editable Match Info */}
      <div className="w-3/4 mb-8">
        <label className="block mb-2 font-medium">Game</label>
        <select
          className="p-2 border border-gray-300 rounded-lg w-full mb-4"
          value={formData.game}
          onChange={(e) => handleDropdownChange(e, "game")}
        >
          <option value="rocket-league">Rocket League</option>
          <option value="valorant">Valorant</option>
          <option value="apex-legends">Apex Legends</option>
        </select>

        <label className="block mb-2 font-medium">Week</label>
        <select
          className="p-2 border border-gray-300 rounded-lg w-full mb-4"
          value={formData.week}
          onChange={(e) => handleDropdownChange(e, "week")}
        >
          <option value="1">Week 1</option>
          <option value="2">Week 2</option>
          <option value="3">Week 3</option>
        </select>

        <label className="block mb-2 font-medium">School</label>
        <input
          type="text"
          value={formData.school}
          className="p-2 border border-gray-300 rounded-lg w-full mb-4"
          readOnly
        />

        <label className="block mb-2 font-medium">Opponent</label>
        <input
          type="text"
          value={formData.opponent}
          className="p-2 border border-gray-300 rounded-lg w-full mb-4"
          readOnly
        />
      </div>

      {/* Editable Player Data */}
      <div className="w-3/4">
        {formData.players.length > 0 ? (
          formData.players.map((player, index) => (
            <div
              key={index}
              className="mb-6 border p-4 rounded-lg bg-white shadow"
            >
              <h3 className="font-bold mb-2">Player: {player.playerName}</h3>
              {Object.entries(player).map(([key, value]) => (
                <div key={key} className="mb-2">
                  <label className="block text-sm font-medium capitalize">
                    {key}
                  </label>
                  <input
                    type="text"
                    value={value}
                    onChange={(e) => handleInputChange(e, index, key)}
                    className="border p-2 w-full"
                    readOnly={key === "playerName" || key === "school"}
                  />
                </div>
              ))}
            </div>
          ))
        ) : (
          <p>No player data available.</p>
        )}
      </div>

      <button
        className="mt-8 bg-green-500 text-white px-6 py-3 rounded-lg hover:bg-green-600 transition"
        onClick={handleSubmit}
      >
        Submit
      </button>
    </div>
  );
};

export default ModifyPage;
