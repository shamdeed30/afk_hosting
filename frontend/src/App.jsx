import "./App.css";
import { Route, Routes } from "react-router-dom";
import DesktopNavbar from "./components/DesktopNavbar";
import HomePage from "./components/HomePage";
import UploadPage from "./components/UploadPage";
import RankingPage from "./components/RankingPage";
import ProfilePage from "./components/ProfilePage";
import ProtectedRoute from "./components/ProtectedRoute";
import ModifyPage from "./components/ModifyPage";

function App() {
  return (
    <div className="App">
      <DesktopNavbar />

      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/ranking" element={<RankingPage />} />
        <Route
          path="/upload"
          element={<ProtectedRoute page={<UploadPage />} />}
        />
        <Route
          path="/modify"
          element={<ProtectedRoute page={<ModifyPage />} />}
        />
        <Route path="/profile" element={<ProfilePage />} />
      </Routes>
    </div>
  );
}

export default App;
