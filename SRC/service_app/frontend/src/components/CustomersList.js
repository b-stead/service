import React, { useEffect, useState } from "react";
import api from "../api/axios";

const CustomersList = () => {
  const [customers, setCustomers] = useState([]); // State to store customers
  const [loading, setLoading] = useState(true); // State to handle loading
  const [error, setError] = useState(null); // State to handle errors

  const sub = "somerandomstring"; // Hardcoded sub value for now

  // Fetch customers from the FastAPI backend
  useEffect(() => {
    const fetchCustomers = async () => {
      try {
        const response = await api.get(`/user/${sub}/customers`);
          setCustomers(response.data); // Update customers state
          console.log("Fetched customers:", response.data);
      } catch (err) {
        console.error("Error fetching customers:", err);
        setError("Failed to fetch customers.");
      } finally {
        setLoading(false); // Set loading to false
      }
    };

    fetchCustomers();
  }, []);

  // Render loading, error, or customer table
  if (loading) {
    return <div className="text-center text-blue-500">Loading...</div>;
  }

  if (error) {
    return <div className="text-center text-red-500">{error}</div>;
  }

  return (
    <div className="p-4">
      <h2 className="text-2xl font-bold mb-4">Customers</h2>
      <table className="table-auto w-full border-collapse border border-gray-300">
        <thead>
          <tr className="bg-gray-100">
            <th className="border border-gray-300 px-4 py-2">ID</th>
            <th className="border border-gray-300 px-4 py-2">Name</th>
            <th className="border border-gray-300 px-4 py-2">Email</th>
            <th className="border border-gray-300 px-4 py-2">Phone</th>
          </tr>
        </thead>
        <tbody>
          {customers.map((customer) => (
            <tr key={customer.id} className="hover:bg-gray-50">
              <td className="border border-gray-300 px-4 py-2">{customer.customer_id}</td>
              <td className="border border-gray-300 px-4 py-2">{customer.name}</td>
              <td className="border border-gray-300 px-4 py-2">{customer.email}</td>
              <td className="border border-gray-300 px-4 py-2">{customer.phone}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default CustomersList;