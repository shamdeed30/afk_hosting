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
    code: "",
    squad_placed: "",
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
    <div className="flex min-h-screen flex-col items-center justify-center bg-gray-100 p-6">
      <h1 className="mb-8 text-4xl font-bold">Modify Game Data</h1>

      {/* Display errors, if any */}
      {error && (
        <div className="mb-6 w-3/4 rounded bg-red-100 p-4 text-red-700">
          {error}
        </div>
      )}

      {/* Editable Match Info */}
      <div className="mb-8 w-3/4">
        <label className="mb-2 block font-medium">Game</label>
        <select
          className="mb-4 w-full rounded-lg border border-gray-300 p-2"
          value={formData.game}
          onChange={(e) => handleDropdownChange(e, "game")}
        >
          <option value="rocket-league">Rocket League</option>
          <option value="valorant">Valorant</option>
          <option value="apex-legends">Apex Legends</option>
        </select>

        <label className="mb-2 block font-medium">Week</label>
        <select
          className="mb-4 w-full rounded-lg border border-gray-300 p-2"
          value={formData.week}
          onChange={(e) => handleDropdownChange(e, "week")}
        >
          <option value="week-1">Week 1</option>
          <option value="week-2">Week 2</option>
          <option value="week- 3">Week 3</option>
        </select>

        {formData.game === "valorant" ? (
          <div>
            <label className="mb-2 block font-medium">Map</label>
            <input
              type="text"
              value={formData.map}
              className="mb-4 w-full rounded-lg border border-gray-300 p-2"
              readOnly
            />
          </div>
        ) : null}

        {formData.game === "apex-legends" ? (
          <div>
            <label className="mb-2 block font-medium">Code</label>
            <input
              type="text"
              value={formData.code}
              className="mb-4 w-full rounded-lg border border-gray-300 p-2"
              readOnly
            />
          </div>
        ) : null}

        {formData.game === "apex-legends" ? (
          <div>
            <label className="mb-2 block font-medium">Squad Placement</label>
            <input
              type="text"
              value={formData.squad_placed}
              className="mb-4 w-full rounded-lg border border-gray-300 p-2"
              readOnly
            />
          </div>
        ) : null}

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
          value={formData.opponent_school}
          className="mb-4 w-full rounded-lg border border-gray-300 p-2"
          readOnly
        />
      </div>

      {/* Editable Player Data */}
      <div className="w-3/4">
        {formData.players.map((player, index) => (
          <div
            key={index}
            className="mb-6 rounded-lg border bg-white p-4 shadow"
          >
            <h3 className="mb-2 font-bold">Player: {player.name}</h3>
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
                  readOnly={["name", "agent", "map"].includes(key)} // Adjust based on which fields are editable
                />
              </div>
            ))}
          </div>
        ))}
      </div>

      <button
        className="mt-8 rounded-lg bg-green-500 px-6 py-3 text-white transition hover:bg-green-600"
        onClick={handleSubmit}
      >
        {loading ? "Submitting..." : "Submit"}
      </button>
    </div>
  );
};

export default ModifyPage;
