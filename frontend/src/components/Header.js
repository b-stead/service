import React from "react";

const Header = ({ title }) => {
  return (
    <header className="bg-primary text-white h-16 p-4 shadow-md">
      <div className="container mx-auto flex justify-between items-center">
        <h1 className="text-xl font-bold">{title}</h1>
        <button className="bg-secondary text-primary px-4 py-2 rounded hover:bg-tertiary">
          Logout
        </button>
      </div>
    </header>
  );
};

export default Header;