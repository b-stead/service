import React, { useEffect, useState } from "react";
import api from "../api/Axios";
import ErrorMessage from "../components/ErrorMessage";

const CustomersList = ({ sub }) => {
  const [customers, setCustomers] = useState([]); // State to store customers
  const [loading, setLoading] = useState(true); // State to handle loading
  const [error, setError] = useState(null); // State to handle errors

  // Fetch customers from the FastAPI backend
  const fetchCustomers = async () => {

    setLoading(true); // Set loading to true before fetching
    setError(null); // Clear any previous errors
    try {
      const response = await api.get(`/user/${sub}/customers`);
      console.log("API Response:", response.data);

      if (Array.isArray(response.data)) {
        setCustomers(response.data); // Update customers state
      } else {
        setError("Unexpected response format.");
      }
    } catch (err) {
      console.error("Error fetching customers:", err);
      setError("Failed to fetch customers. Please try again.");
    } finally {
      setLoading(false); // Set loading to false
    }
  };

  // Fetch customers on component mount
  useEffect(() => {
    fetchCustomers();
  }, [sub]);

  // Render loading state
  if (loading) {
    return <div className="text-center text-blue-500">Loading customers...</div>;
  }

  // Render error state with retry button
  if (error) {
    return (
      <div className="flex items-center justify-center min-h-[200px]">
        <div className="p-6 shadow-md max-w-md text-center">
          <ErrorMessage message={error} />
          <button
            onClick={fetchCustomers} // Retry fetching customers
            className="mt-4 px-4 py-2 bg-secondary text-white rounded hover:bg-quinary"
          >
            Retry
          </button>
        </div>
      </div>
    );
  }

  // Render customer table
  return (
    <section>
      <div class="flex flex-col justify-center h-full w-full">
        <div class="w-full bg-white shadow-lg rounded-sm border border-gray-200">
          <header class="px-5 py-4 border-b border-gray-100">
            <h2 class="font-semibold text-gray-800">Customers</h2>
          </header>
          <div class="p-3">
            <div class="overflow-x-auto">
              <table className="table-auto w-full border-collapse border border-gray-300">
                <thead>
                  <tr className="bg-gray-100">
                    <th className="border border-gray-300 px-4 py-2">ID</th>
                    <th className="border border-gray-300 px-4 py-2">Name</th>
                    <th className="border border-gray-300 px-4 py-2">Email</th>
                    <th className="border border-gray-300 px-4 py-2">Phone</th>
                    <th className="border border-gray-300 px-4 py-2">Job Status</th>
                    <th className="border border-gray-300 px-4 py-2">Payment Status</th>
                    <th className="border border-gray-300 px-4 py-2">Job Status</th>
                    <th className="border border-gray-300 px-4 py-2">Payment Status</th>
                  </tr>
                </thead>
                <tbody>
                  {customers.map((customer) => (
                    <tr key={customer.id} className="hover:bg-gray-50">
                      <td className="border border-gray-300 px-4 py-2">{customer.customer_id}</td>
                      <td className="border border-gray-300 px-4 py-2">{customer.name}</td>
                      <td className="border border-gray-300 px-4 py-2">{customer.email}</td>
                      <td className="border border-gray-300 px-4 py-2">{customer.phone}</td>
                      <td className="border border-gray-300 px-4 py-2">Test Status</td>
                      <td className="border border-gray-300 px-4 py-2">Test Payment</td>
                      <td className="border border-gray-300 px-4 py-2">Test Status</td>
                      <td className="border border-gray-300 px-4 py-2">Test Payment</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};

export default CustomersList;