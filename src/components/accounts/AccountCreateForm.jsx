import { useState } from "react";
import { createAccount } from "../../api/accounts";

export default function AccountCreateForm({ onCreated, onCancel }) {
  const [form, setForm] = useState({
    number: "",
    currency: "CLP",
    per_tx_limit: "200000.00",
    daily_limit: "500000.00",
  });
  const [busy, setBusy] = useState(false);
  const [msg, setMsg] = useState("");

  const handleChange = (e) =>
    setForm((f) => ({ ...f, [e.target.name]: e.target.value }));

  const submit = async (e) => {
    e.preventDefault();
    setBusy(true);
    setMsg("");
    try {
      // balance lo maneja backend (read-only)
      await createAccount({
        number: form.number.trim(),
        currency: form.currency,
        per_tx_limit: form.per_tx_limit,
        daily_limit: form.daily_limit,
      });
      setMsg("✅ Cuenta creada");
      onCreated?.(); // refrescar lista
      onCancel?.();  // cerrar formulario
    } catch (err) {
      const detail = err.response?.data?.detail || "Error al crear cuenta";
      setMsg(`❌ ${detail}`);
    } finally {
      setBusy(false);
    }
  };

  return (
    <form onSubmit={submit} className="space-y-3">
      <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
        <div>
          <label className="block text-sm text-gray-600 mb-1">Número</label>
          <input
            name="number"
            className="border w-full p-2 rounded text-gray-800"
            placeholder="001-0005"
            value={form.number}
            onChange={handleChange}
            required
          />
        </div>
        <div>
          <label className="block text-sm text-gray-600 mb-1">Moneda</label>
          <select
            name="currency"
            className="border w-full p-2 rounded text-gray-800"
            value={form.currency}
            onChange={handleChange}
          >
            <option value="CLP">CLP</option>
            <option value="USD">USD</option>
          </select>
        </div>
        <div>
          <label className="block text-sm text-gray-600 mb-1">Límite por tx</label>
          <input
            name="per_tx_limit"
            type="number"
            step="0.01"
            className="border w-full p-2 rounded text-gray-800"
            value={form.per_tx_limit}
            onChange={handleChange}
          />
        </div>
        <div>
          <label className="block text-sm text-gray-600 mb-1">Límite diario</label>
          <input
            name="daily_limit"
            type="number"
            step="0.01"
            className="border w-full p-2 rounded text-gray-800"
            value={form.daily_limit}
            onChange={handleChange}
          />
        </div>
      </div>

      <div className="flex gap-2">
        <button
          disabled={busy}
          className="bg-emerald-600 text-white px-4 py-2 rounded hover:bg-emerald-700 disabled:opacity-50"
        >
          Crear cuenta
        </button>
        <button
          type="button"
          onClick={onCancel}
          className="bg-gray-200 text-gray-800 px-4 py-2 rounded hover:bg-gray-300"
        >
          Cancelar
        </button>
      </div>

      {msg && <p className="text-sm text-gray-700">{msg}</p>}
    </form>
  );
}
