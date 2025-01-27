import React, { useState } from "react";

const ModifyPage = () => {
  // Mock data for testing the form
  const mockData = {
    game: "RL",
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

  const handleSubmit = async () => {
    try {
      const response = await fetch(`http://localhost:8080/upload_match`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(formData),
      });
      if (response.ok) {
        alert("Data submitted successfully!");
      } else {
        alert("Failed to submit data.");
        console.error("Submission error:", await response.json());
      }
    } catch (error) {
      console.error("Error submitting data:", error);
      alert("Failed to submit data.");
    }
  };

  if (!formData) return <p>Loading match data...</p>;

  return (
    <div className="flex min-h-screen flex-col items-center justify-center bg-gray-100 p-6">
      <h1 className="mb-8 text-4xl font-bold">Modify Game Data</h1>

      {/* Editable Match Info */}
      <div className="mb-8 w-3/4">
        <label className="mb-2 block font-medium">Game</label>
        <select
          className="mb-4 w-full rounded-lg border border-gray-300 p-2"
          value={formData.game}
          onChange={(e) => handleDropdownChange(e, "game")}
        >
          <option value="RL">Rocket League</option>
          <option value="Val">Valorant</option>
          <option value="Apex">Apex Legends</option>
        </select>

        <label className="mb-2 block font-medium">Week</label>
        <select
          className="mb-4 w-full rounded-lg border border-gray-300 p-2"
          value={formData.week}
          onChange={(e) => handleDropdownChange(e, "week")}
        >
          <option value="1">Week 1</option>
          <option value="2">Week 2</option>
          <option value="3">Week 3</option>
        </select>

        <label className="mb-2 block font-medium">School</label>
        <input
          type="text"
          value={formData.school}
          className="mb-4 w-full rounded-lg border border-gray-300 p-2"
          readOnly
        />

        <label className="mb-2 block font-medium">Opponent</label>
        <input
          type="text"
          value={formData.opponent}
          className="mb-4 w-full rounded-lg border border-gray-300 p-2"
          readOnly
        />
      </div>

      {/* Editable Player Data */}
      <div className="w-3/4">
        {formData.players.length > 0 ? (
          formData.players.map((player, index) => (
            <div
              key={index}
              className="mb-6 rounded-lg border bg-white p-4 shadow"
            >
              <h3 className="mb-2 font-bold">Player: {player.playerName}</h3>
              {Object.entries(player).map(([key, value]) => (
                <div key={key} className="mb-2">
                  <label className="block text-sm font-medium capitalize">
                    {key}
                  </label>
                  <input
                    type="text"
                    value={value}
                    onChange={(e) => handleInputChange(e, index, key)}
                    className="w-full border p-2"
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
        className="mt-8 rounded-lg bg-green-500 px-6 py-3 text-white transition hover:bg-green-600"
        onClick={handleSubmit}
      >
        Submit
      </button>
    </div>
  );
};

export default ModifyPage;
