import React from "react";
import JobsList from "../components/JobsList";

const JobsPage = () => {
  const sub = "somerandomstring"; // Hardcoded sub value for now
  return (
    <div>
      <JobsList sub={sub}  /> {/* Render the JobsList component */}
    </div>
  );
};

export default JobsPage;