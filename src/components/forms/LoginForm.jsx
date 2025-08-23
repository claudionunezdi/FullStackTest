import { useState } from "react";
import { login } from "../../api/auth";
import useAuth from "../../hooks/useAuth";

export default function LoginForm() {
    const { login: doLogin } = useAuth();
    const [form, setForm] = useState({ username: "", password: "" });
    const [msg, setMsg] = useState("");

    const handleChange = (e) => setForm({ ...form, [e.target.name]: e.target.value });

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            const res = await login(form);
            doLogin(res.data.access);
            setMsg("Login Exitoso")
        } catch {
            setMsg("Credenciales inválidas");
        }
    };

    return (
        <form onSubmit={handleSubmit}>
            <h2>Login</h2>
            <input name="username" placeholder="Usuario" onChange={handleChange} />
            <input type="password" name="password" placeholder="Contraseña" onChange={handleChange} />
            <button type="submit">Ingresar</button>
            <p>{msg}</p>
        </form>
    )

}