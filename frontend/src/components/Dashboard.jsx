import React from "react";
import { Outlet } from "react-router-dom";
import Topbar from "./Topbar";
import "./Dashboard.css"

function Dashboard() {

  return (
    <div className="Dashboard">
      <Topbar />
      <div className="CurrentPage">
        <Outlet />
      </div>
    </div>
  );
}

export default Dashboard;