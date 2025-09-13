import React from "react";
import { Bars3Icon } from "@heroicons/react/24/outline";
import { useLocation } from "react-router-dom";

const Navbar = ({ isSidebarOpen, onMenuClick }) => {
  const location = useLocation();

  // Extract the current page name from the URL
  const currentPage = location.pathname.split("/").pop(); // Get the last part of the path
  const formattedPageName =
    currentPage.charAt(0).toUpperCase() + currentPage.slice(1); // Capitalize the first letter

  return (
    <header className="bg-gray-200 p-4 mt-2 flex items-center">
      {/* Conditionally Render Burger Icon */}
      {!isSidebarOpen && (
        <button onClick={onMenuClick} className="text-gray-700">
          <Bars3Icon className="h-6 w-6" />
        </button>
      )}
      <div className="ml-4 flex flex-row justify-center">
        <span className="text-sm text-gray-700">Dashboard / </span>
        <span className="text-sm pl-2 font-semibold text-gray-900">
           {formattedPageName}
        </span>
          </div>
          <div className="ml-auto text-sm text-gray-600"> Sign In
            
          </div>
    </header>
  );
};

export default Navbar;