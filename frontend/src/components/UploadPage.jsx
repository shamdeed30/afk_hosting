import React, { useState } from "react";
import { useNavigate } from "react-router-dom";

const UploadPage = () => {
  const [file, setFile] = useState(null);
  const [game, setGame] = useState("");
  const [week, setWeek] = useState("");
  const [school, setSchool] = useState("");
  const [opponent_school, setOpponentSchool] = useState("");
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const handleFileChange = (event) => {
    setFile(event.target.files[0]);
  };

  const handleDrop = (event) => {
    event.preventDefault();
    const files = event.dataTransfer.files;
    if (files.length > 0) {
      setFile(files[0]);
    }
  };

  const handleDragOver = (event) => {
    event.preventDefault();
  };

  const handleSubmit = async () => {
    if (!file || !game || !week || !school || !opponent_school) {
      alert("Please fill all the fields and upload a file.");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);
    formData.append("game", game);
    formData.append("week", week);
    formData.append("school", school);
    formData.append("opponent_school", opponent_school);

    setLoading(true); //Start the loading animation

    try {
      const response = await fetch("http://127.0.0.1:8080/upload_file", {
        method: "POST",
        body: formData,
      });

      if (response.ok) {
        const ocrData = await response.json();
        navigate("/modify", { state: { ocrData } });
      } else {
        console.error("File upload failed.");
        alert("Failed to process the file.");
      }
    } catch (error) {
      console.error("Error uploading file:", error);
      alert("An error occurred while uploading the file.");
    } finally {
      setLoading(false); //Stop the loading animation
    }
  };

  return (
    <div className="flex min-h-screen flex-col items-center justify-center bg-gray-100 p-6">
      <h1 className="mb-8 text-4xl font-bold">Upload Game</h1>
      <div
        className="flex h-64 w-3/4 flex-col items-center justify-center rounded-lg border-2 border-dashed border-gray-400 bg-white p-4 hover:shadow-lg"
        onDrop={handleDrop}
        onDragOver={handleDragOver}
      >
        {file ? (
          <p className="text-center text-gray-600">{file.name}</p>
        ) : (
          <p className="text-center text-gray-600">
            Drag and drop your file here or{" "}
            <label className="cursor-pointer text-blue-500">
              browse
              <input
                type="file"
                className="hidden"
                onChange={handleFileChange}
              />
            </label>
          </p>
        )}
      </div>

      <div className="mt-8 grid w-3/4 grid-cols-1 gap-4 sm:grid-cols-3">
        <select
          className="rounded-lg border border-gray-300 p-4"
          value={game}
          onChange={(e) => setGame(e.target.value)}
        >
          <option value="">Select Game</option>
          <option value="rocket-league">Rocket League</option>
          <option value="valorant">Valorant</option>
          <option value="apex-legends">Apex Legends</option>
        </select>

        <select
          className="rounded-lg border border-gray-300 p-4"
          value={week}
          onChange={(e) => setWeek(e.target.value)}
        >
          <option value="">Select Week</option>
          <option value="week-1">Week 1</option>
          <option value="week-2">Week 2</option>
          <option value="week-3">Week 3</option>
        </select>

        <select
          className="rounded-lg border border-gray-300 p-4"
          value={team}
          onChange={(e) => setTeam(e.target.value)}
        >
          <option value="">Select Team</option>
          <option value="team-a">Team A</option>
          <option value="team-b">Team B</option>
          <option value="team-c">Team C</option>
        </select>
      </div>

      <button
        className="mt-8 rounded-lg bg-blue-500 px-6 py-3 text-white transition hover:bg-blue-600"
        onClick={handleSubmit}
      >
        Submit
      </button>
    </div>
  );
};

export default UploadPage;
