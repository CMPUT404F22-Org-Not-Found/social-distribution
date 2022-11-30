import React from "react";
import { Navigate, Outlet } from "react-router-dom"

function ProtectedRoute() {
    const authToken = localStorage.getItem("auth-token");
    console.log("Is Protected:", authToken);

    if (authToken) {
        return <Outlet />
    }
    return (
         <Navigate to="/" replace />
    );
}

export default ProtectedRoute;