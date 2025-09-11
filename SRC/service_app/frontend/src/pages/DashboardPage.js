import React, {useState} from "react";
import Sidebar from "../components/Sidebar";
import Header from "../components/Header";
import CustomersList from "../components/CustomersList";
import JobsList from "../components/JobsList";
import InvoicesList from "../components/InvoicesList";

const DashboardPage = () => {
  const [view, setView] = useState("customers"); // Default view is "customers"

  // Render the appropriate component based on the selected view
  const renderContent = () => {
    switch (view) {
      case "customers":
        return <CustomersList />;
      case "jobs":
        return <JobsList />;
      case "invoices":
        return <InvoicesList />;
      default:
        return <CustomersList />;
    }
  };

  return (
    <div className="flex">
      {/* Sidebar */}
      <Sidebar setView={setView} />

      {/* Main Content */}
      <div className="flex-1">
        {/* Header */}
        <Header title="Dashboard" />

        {/* Content */}
        <div className="p-6 bg-tertiary text-primary">{renderContent()}</div>
      </div>
    </div>
  );
};

export default DashboardPage;