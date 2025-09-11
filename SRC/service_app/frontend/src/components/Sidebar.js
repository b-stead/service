import React from "react";
import { Link } from "react-router-dom";

const Sidebar = ({ setView}) => {
  return (
    <div className="w-56 bg-primary text-white h-screen flex flex-col">
      {/* Logo Section */}
      <div className="h-16 bg-secondary flex items-center justify-center">
        <img
          src="/path-to-your-logo.png" // Replace with your logo path
          alt="Logo"
          className="h-10 w-auto"
        />
      </div>

      {/* Navigation Links */}
      <nav className="p-4 flex-1">
        <ul>
          <li className="mb-4">
            <button
              onClick={() => setView("customers")}
              className="hover:text-tertiary"
            >
              Manage Customers
            </button>
          </li>
          <li className="mb-4">
            <button
              onClick={() => setView("jobs")}
              className="hover:text-tertiary"
            >
              Manage Jobs
            </button>
          </li>
          <li className="mb-4">
            <button
              onClick={() => setView("invoices")}
              className="hover:text-tertiary"
            >
              Manage Invoices
            </button>
          </li>
        </ul>
      </nav>
    </div>
  );
};

export default Sidebar;