import React from "react";
import { NavLink, Link } from "react-router-dom";
import { XMarkIcon } from "@heroicons/react/24/outline"; // Ensure you have Heroicons installed

const Sidebar = ({ isOpen, onClose }) => {
  const links = [
    { name: "Customers", path: "/dashboard/customers" },
    { name: "Jobs", path: "/dashboard/jobs" },
    { name: "Invoices", path: "/dashboard/invoices" },
  ];

  return (
    <aside
      className={`fixed inset-0 z-50 my-4 ml-4 h-[calc(100vh-32px)] w-72 rounded-xl transition-transform duration-300 ${
        isOpen ? "translate-x-0" : "-translate-x-80"
      } border border-blue-gray-100 bg-primary text-black`}
    >
      {/* Close Button */}
      <div className="flex justify-between items-center p-4">
        {/* Dashboard Header as a Link */}
        <Link to="/dashboard" className="text-center font-bold text-lg text-white hover:underline">
          Dashboard
        </Link>
        <button onClick={onClose} className="text-white">
          <XMarkIcon className="h-6 w-6" />
        </button>
      </div>

      {/* Navigation Links */}
      <nav className="mt-4">
        <ul className="space-y-2 mx-4">
          {links.map((link) => (
            <li key={link.name} className="mb-2 text-white">
              <NavLink
                to={link.path}
                className={({ isActive }) =>
                  `block px-4 py-2 rounded ${
                    isActive
                      ? "bg-tertiary text-black" // Active: background and black text
                      : "text-white hover:bg-secondary hover:text-black" // Inactive: white text, black on hover
                  }`
                }
              >
                {link.name}
              </NavLink>
            </li>
          ))}
        </ul>
      </nav>
    </aside>
  );
};

export default Sidebar;