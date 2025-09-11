import React from "react";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import CustomersPage from "./pages/CustomersPage1";
import DashboardPage from "./pages/DashboardPage";
import HomePage from "./pages/HomePage";

const App = () => {
  return (
    <Router>
      <Routes>
      <Route path="/" element={<HomePage />} />
      <Route path="/dashboard" element={<DashboardPage />} />
      <Route path="/admin/customers" element={<CustomersPage />} />
    </Routes>
    </Router>
  );
};

export default App;