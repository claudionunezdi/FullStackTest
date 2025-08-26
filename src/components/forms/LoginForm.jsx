import { useState } from "react";
import { login as loginApi } from "../../api/auth";
import useAuth from "../../hooks/useAuth";
import { useNavigate } from "react-router-dom";

export default function LoginForm() {
  const { login } = useAuth();         // del contexto
  const navigate = useNavigate();
  const [form, setForm] = useState({ username: "", password: "" });
  const [msg, setMsg] = useState("");

  const handleChange = (e) =>
    setForm({ ...form, [e.target.name]: e.target.value });

  const handleSubmit = async (e) => {
    e.preventDefault();
    setMsg("");
    try {
      const res = await loginApi(form);
      console.log("LOGIN OK:", res.data);
      login(res.data.access, res.data.refresh); // guarda ambos
      setMsg("✅ Login exitoso");
      navigate("/dashboard");
    } catch (err) {
      console.error("LOGIN ERROR:", err.response?.data || err.message);
      setMsg("❌ Credenciales inválidas");
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <input
        className="border w-full p-2 rounded text-gray-800"
        name="username"
        placeholder="Usuario"
        onChange={handleChange}
      />
      <input
        className="border w-full p-2 rounded text-gray-800"
        type="password"
        name="password"
        placeholder="Contraseña"
        onChange={handleChange}
      />
      <button
        className="bg-blue-600 w-full text-white py-2 rounded hover:bg-blue-700"
        type="submit"
      >
        Ingresar
      </button>
      {msg && <p className="text-center text-sm text-gray-700">{msg}</p>}
    </form>
  );
}
