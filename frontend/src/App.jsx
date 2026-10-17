import React from "react";

import {
  BrowserRouter,
  Routes,
  Route,
} from "react-router-dom";

import LandingPage from "./pages/LandingPage";
import UploadPage from "./pages/UploadPage";
import ResultsPage from "./pages/ResultsPage";
import Dashboard from "./pages/Dashboard";


function App() {
  return (
    <BrowserRouter>

      <Routes>

        {/* Landing Page */}

        <Route
          path="/"
          element={<LandingPage />}
        />


        {/* Resume Upload */}

        <Route
          path="/upload"
          element={<UploadPage />}
        />


        {/* Analysis Results */}

        <Route
          path="/results"
          element={<ResultsPage />}
        />


        {/* Dashboard */}

        <Route
          path="/dashboard"
          element={<Dashboard />}
        />

      </Routes>

    </BrowserRouter>
  );
}


export default App;