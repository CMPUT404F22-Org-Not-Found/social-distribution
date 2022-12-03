import React from "react";
import { Navigate, Outlet } from "react-router-dom";

function RedirectIfLoggedIn() {
    const authToken = window.localStorage.getItem("auth-token");

    if (authToken) {
        return (<Navigate to="/" replace />)
    }
    return (
        <Outlet />
    );
}

export default RedirectIfLoggedIn;