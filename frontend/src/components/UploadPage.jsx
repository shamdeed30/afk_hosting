import React, { useState } from "react";
import { useNavigate } from "react-router-dom";

const UploadPage = () => {
    const [file, setFile] = useState(null);
    const [game, setGame] = useState("");
    const [week, setWeek] = useState("");
    const [team, setTeam] = useState("");
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
        if (!file || !game || !week || !team) {
          alert("Please fill all the fields and upload a file.");
          return;
        }
    
        const formData = new FormData();
        formData.append("file", file);
        formData.append("game", game);
        formData.append("week", week);
        formData.append("team", team);
    
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
        }
      };

    return (
        <div className="flex flex-col items-center justify-center min-h-screen bg-gray-100 p-6">
            <h1 className="text-4xl font-bold mb-8">Upload Game</h1>
            <div
                className="flex flex-col items-center justify-center w-3/4 h-64 border-2 border-dashed border-gray-400 rounded-lg bg-white p-4 hover:shadow-lg"
                onDrop={handleDrop}
                onDragOver={handleDragOver}
            >
                {file ? (
                    <p className="text-center text-gray-600">{file.name}</p>
                ) : (
                    <p className="text-center text-gray-600">
                        Drag and drop your file here or{" "}
                        <label className="text-blue-500 cursor-pointer">
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

            <div className="mt-8 w-3/4 grid grid-cols-1 gap-4 sm:grid-cols-3">
                <select
                    className="p-4 border border-gray-300 rounded-lg"
                    value={game}
                    onChange={(e) => setGame(e.target.value)}
                >
                    <option value="">Select Game</option>
                    <option value="rocket-league">Rocket League</option>
                    <option value="valorant">Valorant</option>
                    <option value="apex-legends">Apex Legends</option>
                </select>

                <select
                    className="p-4 border border-gray-300 rounded-lg"
                    value={week}
                    onChange={(e) => setWeek(e.target.value)}
                >
                    <option value="">Select Week</option>
                    <option value="week-1">Week 1</option>
                    <option value="week-2">Week 2</option>
                    <option value="week-3">Week 3</option>
                </select>

                <select
                    className="p-4 border border-gray-300 rounded-lg"
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
                className="mt-8 bg-blue-500 text-white px-6 py-3 rounded-lg hover:bg-blue-600 transition"
                onClick={handleSubmit}
            >
                Submit
            </button>
        </div>
    );
};

export default UploadPage;