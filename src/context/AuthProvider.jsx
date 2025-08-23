import { createContext, useState, useEffect } from "react";

export const AuthContext = createContext();


export function AuthProvider({ children }) {
    const [user, setUser] = useState(null);
    const [token, setToken] = useState(localStorage.getItem("access"));

    const login = (data) => {
        setToken(data.access);
        localStorage.setItem("access", data.access);
    };

    const logout = () => {
        setToken(null);
        localStorage.removeItem("access");
    };

    return (
        <AuthContext.Provider value={{ user, token, login, logout }}>
            {children}
        </AuthContext.Provider>
    );
}