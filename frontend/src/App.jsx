import React from "react";

import {
  BrowserRouter,
  Routes,
  Route,
} from "react-router-dom";

import LandingPage from "./pages/LandingPage";
import UploadPage from "./pages/UploadPage";
import ResultsPage from "./pages/ResultsPage";


function App() {
  return (
    <BrowserRouter>

      <Routes>

        <Route
          path="/"
          element={<LandingPage />}
        />

        <Route
          path="/upload"
          element={<UploadPage />}
        />

        <Route
          path="/results"
          element={<ResultsPage />}
        />

      </Routes>

    </BrowserRouter>
  );
}


export default App;