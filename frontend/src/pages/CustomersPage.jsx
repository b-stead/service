import React from "react";
import CustomersList from "../components/CustomersList";

const CustomersPage = () => {
  const sub = "somerandomstring"; // Hardcoded sub value for now
  return (
    <div className="p-4">
      {/* Action Boxes Row */}
      <div className="grid grid-cols-4 gap-4 mb-6">
        <div className="p-4 bg-blue-500 text-white text-center rounded shadow hover:bg-blue-600 cursor-pointer">
          Action 1
        </div>
        <div className="p-4 bg-green-500 text-white text-center rounded shadow hover:bg-green-600 cursor-pointer">
          Action 2
        </div>
        <div className="p-4 bg-yellow-500 text-white text-center rounded shadow hover:bg-yellow-600 cursor-pointer">
          Action 3
        </div>
        <div className="p-4 bg-red-500 text-white text-center rounded shadow hover:bg-red-600 cursor-pointer">
          Action 4
        </div>
      </div>

      {/* Jobs List Section */}
      <CustomersList sub={sub}  /> {/* Render the CustomersList component */}
    </div>
  );
};

export default CustomersPage;