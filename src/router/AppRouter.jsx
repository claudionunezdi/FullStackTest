import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import LoginPage from "../pages/LoginPage";
import RegisterPage from "../pages/RegisterPage";
import DashboardPage from "../pages/DashboardPage";
import { useContext } from "react";
import { AuthContext } from "../context/AuthProvider";

export default function AppRouter() {
    const { token } = useContext(AuthContext);

    return (
        <BrowserRouter>
            <Routes>
                <Route path="/login" element={<LoginPage />} />
                <Route path="register" element={<RegisterPage />} />
                <Route path="/dashboard"
                    element={token ? <DashboardPage /> : <Navigate to="/login" />} />
            </Routes>
        </BrowserRouter>
    );
}