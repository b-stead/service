import React from "react";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import DashboardLayout from "./layouts/DashboardLayout";
import AuthLayout from "./layouts/AuthLayout";
import CustomersPage from "./pages/CustomersPage";
import JobsPage from "./pages/JobsPage";
import InvoicesPage from "./pages/InvoicesPage";
import HomePage from "./pages/HomePage"; // Main landing page
import DashboardHome from "./pages/DashboardHome"; // Default dashboard page
import LoginPage from "./pages/LoginPage";
import SignupPage from "./pages/SignupPage";

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
        {/* Auth Layout */}
        <Route path="/auth" element={<AuthLayout />}>
          <Route index element={<LoginPage />} />
          <Route path="signup" element={<SignupPage />} />
        </Route>
      </Routes>
    </Router>
  );
};

export default App;