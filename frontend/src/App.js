import React from "react";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import DashboardLayout from "./layouts/DashboardLayout";
import CustomersPage from "./pages/CustomersPage";
import JobsPage from "./pages/JobsPage";
import InvoicesPage from "./pages/InvoicesPage";
import HomePage from "./pages/HomePage"; // Main landing page
import DashboardHome from "./pages/DashboardHome"; // Default dashboard page

const App = () => {
  return (
    <Router>
      <Routes>
        {/* Main Landing Page */}
        <Route path="/" element={<HomePage />} />

        {/* Dashboard Layout */}
        <Route path="/dashboard" element={<DashboardLayout />}>
          <Route index element={<DashboardHome />} /> {/* Default dashboard page */}
          <Route path="customers" element={<CustomersPage />} />
          <Route path="jobs" element={<JobsPage />} />
          <Route path="invoices" element={<InvoicesPage />} />
        </Route>
      </Routes>
    </Router>
  );
};

export default App;