import React, { useState } from "react";
import { Outlet } from "react-router-dom";
import Sidebar from "../components/Sidebar";
import Navbar from "../components/Navbar";

const DashboardLayout = () => {
  const [isSidebarOpen, setIsSidebarOpen] = useState(true); // State to control sidebar visibility

  return (
    <div className="relative bg-gray-200 h-full">
      {/* Sidebar */}
      <Sidebar isOpen={isSidebarOpen} onClose={() => setIsSidebarOpen(false)} />

      {/* Main Content */}
      <div
        className={`flex flex-col transition-all duration-300 ${
          isSidebarOpen ? "ml-80" : "ml-0"
        } mt-4 min-h-screen`}
      >
        {/* Navbar */}
        <Navbar
            isSidebarOpen={isSidebarOpen}
            onMenuClick={() => setIsSidebarOpen(true)} />

        {/* Page Content */}
        <main className="flex-1 p-6 bg-gray-200">
          <Outlet />
        </main>
        {/* Footer */}
        <footer className="bg-gray-300 p-4 text-center text-sm text-gray-600">
          © 2023 Service App. All rights reserved.
        </footer>
      </div>
    </div>
  );
};

export default DashboardLayout;