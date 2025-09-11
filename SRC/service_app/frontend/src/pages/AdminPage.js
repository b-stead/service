import React from "react";
import Sidebar from "../components/Sidebar";

const AdminPage = () => {
  return (
    <div className="flex">
      <Sidebar />
      <div className="flex-1 p-6">
        <h1 className="text-2xl font-bold">Admin Panel</h1>
        <p>Welcome to the admin panel. Use the sidebar to navigate.</p>
      </div>
    </div>
  );
};

export default AdminPage;