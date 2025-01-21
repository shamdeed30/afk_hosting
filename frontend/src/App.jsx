import "./App.css";
import { Route, Routes } from "react-router-dom";
import DesktopNavbar from "./components/DesktopNavbar";
import HomePage from "./components/HomePage";
import UploadPage from "./components/UploadPage";

function App() {
  return (
    <div className="App">
      <DesktopNavbar />

      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/upload" element={<UploadPage />} />
        <Route path="/modify" element={<HomePage />} />
        <Route path="/profile" element={<HomePage />} />
      </Routes>
    </div>
  );
}

export default App;
