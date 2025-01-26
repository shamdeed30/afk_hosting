import React, { useState } from "react";

const UploadPage = () => {
  const [file, setFile] = useState(null);
  const [game, setGame] = useState("");
  const [week, setWeek] = useState("");
  const [team, setTeam] = useState("");

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

  const handleSubmit = () => {
    // TODO: Add submission logic here
    console.log({ file, game, week, team });
    alert("Submitted successfully!");
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
