import React from "react";

const DashboardHome = () => {
  return (
    <div className="bg-gray-100 h-full flex flex-col justify-center items-center">
      <h1 className="text-3xl font-bold mb-4">Welcome to Your Dashboard</h1>
      <p className="text-gray-700 text-center">
        Use the sidebar to navigate to different sections like Customers, Jobs, and Invoices.
      </p>
    </div>
  );
};

export default DashboardHome;