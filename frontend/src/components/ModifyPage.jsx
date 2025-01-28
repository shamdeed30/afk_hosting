import React, { useState } from "react";
import { useLocation, useNavigate } from "react-router-dom";

const ModifyPage = () => {
  const location = useLocation();
  const navigate = useNavigate();

  // Accept OCR data passed from UploadPage or set default empty structure
  const initialData = location.state?.ocrData || {
    game: "",
    week: "",
    team: "",
    map: "",
    players: [],
  };

  const [formData, setFormData] = useState(initialData);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

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

  // Handle submission of the updated data to the backend
  const handleSubmit = async () => {
    setLoading(true);
    setError("");

    try {
      const response = await fetch("http://127.0.0.1:8080/upload_match", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(formData),
      });

      if (response.ok) {
        alert("Data submitted successfully!");
        navigate("/"); // Navigate back to home or another page after successful submission
      } else {
        const errorData = await response.json();
        setError(errorData.error || "Failed to submit data.");
      }
    } catch (err) {
      console.error("Error submitting data:", err);
      setError("An error occurred while submitting the data.");
    } finally {
      setLoading(false);
    }
  };

  if (loading) return <p>Loading...</p>;
  if (!formData || !formData.players || formData.players.length === 0)
    return <p>No data available. Please upload data first.</p>;

  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-gray-100 p-6">
      <h1 className="text-4xl font-bold mb-8">Modify Game Data</h1>

      {/* Display errors, if any */}
      {error && (
        <div className="mb-6 w-3/4 bg-red-100 text-red-700 p-4 rounded">
          {error}
        </div>
      )}

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

        <label className="block mb-2 font-medium">Map</label>
        <input
          type="text"
          value={formData.map}
          className="p-2 border border-gray-300 rounded-lg w-full mb-4"
          readOnly
        />

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
        {formData.players.map((player, index) => (
          <div
            key={index}
            className="mb-6 border p-4 rounded-lg bg-white shadow"
          >
            <h3 className="font-bold mb-2">Player: {player.name}</h3>
            {Object.entries(player).map(([key, value]) => (
              <div key={key} className="mb-2">
                <label className="block text-sm font-medium capitalize">{key}</label>
                <input
                  type="text"
                  value={value}
                  onChange={(e) => handleInputChange(e, index, key)}
                  className="border p-2 w-full"
                  readOnly={["name", "agent", "map"].includes(key)} // Adjust based on which fields are editable
                />
              </div>
            ))}
          </div>
        ))}
      </div>

      <button
        className="mt-8 bg-green-500 text-white px-6 py-3 rounded-lg hover:bg-green-600 transition"
        onClick={handleSubmit}
      >
        {loading ? "Submitting..." : "Submit"}
      </button>
    </div>
  );
};

export default ModifyPage;
