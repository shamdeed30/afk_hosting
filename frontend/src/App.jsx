import "./App.css";
import { Route, Routes } from "react-router-dom";
import DesktopNavbar from "./components/DesktopNavbar";
import HomePage from "./components/HomePage";

function App() {
  return (
    <div className="App">
      <DesktopNavbar />

      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/upload" element={<HomePage />} />
        <Route path="/modify" element={<HomePage />} />
        <Route path="/profile" element={<HomePage />} />
      </Routes>
    </div>
  );
}

export default App;
