import React from "react";
import { Link } from "react-router-dom";

const HomePage = () => {
  return (
    <div className="bg-tertiary text-white h-screen flex flex-col justify-center items-center">
      <h1 className="text-4xl font-bold mb-6">Welcome to the Service App</h1>
      <p className="text-white mb-4">
        Manage your customers and services efficiently.
      </p>
      <Link
        to="/dashboard"
        className="bg-accent_dark text-white px-6 py-3 rounded hover:bg-tertiary"
      >
        Go to Dashboard
      </Link>
    </div>
  );
};

export default HomePage;