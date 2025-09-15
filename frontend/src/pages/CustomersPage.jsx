import React from "react";
import CustomersList from "../components/CustomersList";

const CustomersPage = () => {
  const sub = "somerandomstring"; // Hardcoded sub value for now
  return (
    <div>
      <CustomersList sub={sub}  /> {/* Render the CustomersList component */}
    </div>
  );
};

export default CustomersPage;