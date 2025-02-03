const API_BASE_URL = "http://40.85.147.30:8080";

const API_ENDPOINTS = {
  getPlayerStats: (game, playerName) =>
    `${API_BASE_URL}/player/${game}?player=${encodeURIComponent(playerName)}`,
  getGameReports: (game, week) => `${API_BASE_URL}/stats/${game}/${week}`,
  uploadFile: `${API_BASE_URL}/upload_file`,
  uploadMatch: `${API_BASE_URL}/upload_match`,
};

export { API_BASE_URL, API_ENDPOINTS };
