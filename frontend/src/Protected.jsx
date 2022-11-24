import React from "react";
import { Navigate, Outlet } from "react-router-dom"

function ProtectedRoute() {
    const authToken = window.localStorage.getItem("auth-token");

    if (authToken) {
        return <Outlet />
    }
    return (
         <Navigate to="/" replace />
    );
}

export default ProtectedRoute;