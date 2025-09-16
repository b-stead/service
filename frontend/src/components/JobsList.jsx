import React, { useEffect, useState } from "react";
import api from "../api/Axios";
import ErrorMessage from "../components/ErrorMessage";

const JobsList = ({ sub }) => {
    const [jobs, setJobs] = useState([]); // State to store jobs
    const [loading, setLoading] = useState(true); // State to handle loading
    const [error, setError] = useState(null); // State to handle errors

    // Fetch jobs from the FastAPI backend
    const fetchJobs = async () => {
        setLoading(true); // Set loading to true before fetching
        setError(null); // Clear any previous errors
        try {
            const response = await api.get(`/user/${sub}/jobs-customer/`);
            console.log("API Response:", response.data);

            if (Array.isArray(response.data)) {
                setJobs(response.data); // Update jobs state
            } else {
                setError("Unexpected response format.");
            }
        } catch (err) {
            console.error("Error fetching jobs:", err);
            setError("Failed to fetch jobs. Please try again.");
        } finally {
            setLoading(false); // Set loading to false
        }
    };
    // Fetch jobs on component mount
    useEffect(() => {
        fetchJobs();
    }, [sub]);
    // Render loading state
    if (loading) {
        return <div className="text-center text-blue-500">Loading jobs...</div>;
    }
    // Render error state with retry button
    if (error) {
        return (
            <div className="flex items-center justify-center min-h-[200px]">
                <div className="p-6 shadow-md max-w-md text-center">
                    <ErrorMessage message={error} />
                    <button
                        onClick={fetchJobs} // Retry fetching jobs
                        className="mt-4 px-4 py-2 bg-secondary text-white rounded hover:bg-quinary"
                    >
                        Retry
                    </button>
                </div>
            </div>
        );
    }
    // Render jobs table
    return (
        <section>
            <div class="flex flex-col justify-center h-full w-full">
                <div class="w-full bg-white shadow-lg rounded-lg border border-gray-200">
                    <header class="px-5 py-4 border-b border-gray-100">
                        <h2 class="font-semibold text-gray-800">Customers</h2>
                    </header>
                    <div class="p-3">
                        <div class="overflow-x-auto">
                            <table className="table-auto w-full border-collapse border border-gray-300">
                                <thead>
                                    <tr>
                                        <th className="py-2 px-4 border-b">Job ID</th>
                                        <th className="py-2 px-4 border-b">Title</th>
                                        <th className="py-2 px-4 border-b">Description</th>
                                        <th className="py-2 px-4 border-b">Status</th>
                                        <th className="py-2 px-4 border-b">Created At</th>
                                        <th className="py-2 px-4 border-b">Updated At</th>
                                        <th className="py-2 px-4 border-b">Value</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    {jobs.map((job) => (
                                        <tr key={job.id} className="hover:bg-gray-100">
                                            <td className="py-2 px-4 border-b">{job.customer_name}</td>
                                            <td className="py-2 px-4 border-b">{job.job_title}</td>
                                            <td className="py-2 px-4 border-b">{job.job_description}</td>
                                            <td className="py-2 px-4 border-b">{job.job_status}</td>
                                            <td className="py-2 px-4 border-b">{new Date(job.start_date).toISOString().split('T')[0]} {/* Outputs YYYY-MM-DD */}</td>
                                            <td className="py-2 px-4 border-b">{new Date(job.end_date).toISOString().split('T')[0]}</td>
                                            <td className="py-2 px-4 border-b">{job.total_amount}</td>
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

export default JobsList;