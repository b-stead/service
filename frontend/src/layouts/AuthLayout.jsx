import React from "react";
import { Outlet } from "react-router-dom";

const AuthLayout = () => {
  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-200">
      <div className="w-full max-w-md bg-quinary p-8 rounded-lg shadow-md">
        <Outlet /> {/* Render the specific auth page here */}
      </div>
    </div>
  );
};

export default AuthLayout;