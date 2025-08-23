import { useState } from "react";
import { register } from "../../api/auth";

export default function RegisterForm() {
    const [form, setForm] = useState({ username: "", email: "", password: "" });
    const [msg, setMsg] = useState("");
    
    const handleChange = (e) => setForm({ ...form, [e.target.name]: e.target.value });

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            await register(form);
            setMsg("Usuario registrado");
        } catch {
            setMsg("Error al registrar")
        }
    };

    return (
        <form onSubmit={handleSubmit}>
            <h2>Registro</h2>
            <input name="username" placeholder="Usuario" onChange={handleChange} />
            <input name="email" placeholder="Email" onChange={handleChange} />
            <input type="password" name="password" placeholder="Contraseña" onChange={handleChange} />
            <button type="submit">Registrarse</button>
            <p>{msg}</p>
        </form>
    );

}