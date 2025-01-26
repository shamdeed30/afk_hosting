import "./App.css";
import { Route, Routes } from "react-router-dom";
import DesktopNavbar from "./components/DesktopNavbar";
import HomePage from "./components/HomePage";
import UploadPage from "./components/UploadPage";
import RankingPage from "./components/RankingPage";
import ProfilePage from "./components/ProfilePage";
import ModifyPage from "./components/ModifyPage";

function App() {
  return (
    <div className="App">
      <DesktopNavbar />

      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/ranking" element={<RankingPage />} />
        <Route path="/upload" element={<UploadPage />} />
        <Route path="/modify" element={<ModifyPage />} />
        <Route path="/modify" element={<HomePage />} />
        <Route path="/profile" element={<ProfilePage />} />
      </Routes>
    </div>
  );
}

export default App;
