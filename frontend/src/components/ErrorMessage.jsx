import React from "react";

const ErrorMessage = ({ message }) => {
  return (
    <div className="p-4 text-center bg-red-400 rounded-md">
      <div className="mb-4 bg-red-300 p-2 rounded-md">
        <p className="text-red-700 font-semibold">{message}</p>
      </div>
    </div>
  );
};

export default ErrorMessage;