import { useEffect, useState } from "react";
import useAuth from "../hooks/useAuth";
import { fetchAccounts } from "../api/accounts";
import AccountList from "../components/accounts/AccountList";
import AccountCreateForm from "../components/accounts/AccountCreateForm";
import MovementPanel from "../components/movements/movementPanel";

export default function DashboardPage() {
  const { logout } = useAuth();
  const [accounts, setAccounts] = useState([]);
  const [selected, setSelected] = useState(null);
  const [showCreate, setShowCreate] = useState(false);

  const load = () =>
    fetchAccounts()
      .then((r) => {
        setAccounts(r.data);
        // si no hay selección, selecciona la primera
        if (!selected && r.data.length) setSelected(r.data[0]);
      })
      .catch(() => setAccounts([]));

  useEffect(() => { load(); }, []);

  return (
    <div className="min-h-screen bg-gray-100 p-4 md:p-6">
      <div className="flex items-center justify-between mb-6">
        <h1 className="text-2xl md:text-3xl font-bold">Mi Banca</h1>
        <button
          onClick={logout}
          className="bg-red-600 text-white px-4 py-2 rounded hover:bg-red-700"
        >
          Cerrar sesión
        </button>
      </div>

      <div className="grid gap-6 md:grid-cols-3">
        {/* Columna izquierda */}
        <div className="md:col-span-1 space-y-4">
          <div className="bg-white rounded-lg shadow-md p-4">
            <div className="flex items-center justify-between mb-3">
              <h2 className="text-lg font-semibold">Mis cuentas</h2>
              {!showCreate && (
                <button
                  onClick={() => setShowCreate(true)}
                  className="text-sm bg-blue-600 text-white px-3 py-1 rounded hover:bg-blue-700"
                >
                  Nueva cuenta
                </button>
              )}
            </div>

            {showCreate ? (
              <AccountCreateForm
                onCreated={load}
                onCancel={() => setShowCreate(false)}
              />
            ) : (
              <AccountList
                accounts={accounts}
                selectedId={selected?.id}
                onSelect={(acc) => setSelected(acc)}
              />
            )}
          </div>
        </div>

        {/* Columna derecha (más ancha) */}
        <div className="md:col-span-2">
          <MovementPanel account={selected} onChanged={load} />
        </div>
      </div>
    </div>
  );
}
