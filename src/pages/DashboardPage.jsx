import { useEffect, useState } from "react";
import API from "../api/api";
import useAuth from "../hooks/useAuth";

export default function DashboardPage() {
  const { logout } = useAuth();
  const [accounts, setAccounts] = useState([]);

  useEffect(() => {
    API.get("/accounts/")
      .then((res) => setAccounts(res.data))
      .catch(() => setAccounts([]));
  }, []);

  return (
    <div>
      <h1>Mis cuentas</h1>
      <button onClick={logout}>Cerrar sesión</button>
      <ul>
        {accounts.map((acc) => (
          <li key={acc.id}>
            {acc.number} — {acc.balance} {acc.currency}
          </li>
        ))}
      </ul>
    </div>
  );
}
