import { useState } from "react";
import { deposit, withdraw } from "../../api/accounts";

export default function MovementPanel({ account, onChanged }) {
  const [tab, setTab] = useState("deposit"); // deposit | withdraw | transfer
  const [amount, setAmount] = useState("");
  const [busy, setBusy] = useState(false);
  const [msg, setMsg] = useState("");

  const canOperate = Boolean(account?.id);

  const doDeposit = async () => {
    setBusy(true); setMsg("");
    try {
      await deposit(account.id, amount, "WEB");
      setMsg("✅ Depósito realizado");
      setAmount("");
      onChanged?.();
    } catch (err) {
      setMsg(`❌ ${err.response?.data?.detail || "Error al depositar"}`);
    } finally {
      setBusy(false);
    }
  };

  const doWithdraw = async () => {
    setBusy(true); setMsg("");
    try {
      await withdraw(account.id, amount, "WEB");
      setMsg("✅ Retiro realizado");
      setAmount("");
      onChanged?.();
    } catch (err) {
      // mapeos: 402 fondos insuficientes, 409 inactiva, 429 límite diario
      const d = err.response?.data?.detail;
      setMsg(`❌ ${d || "Error al retirar"}`);
    } finally {
      setBusy(false);
    }
  };

  return (
    <div className="bg-white rounded-lg shadow-md p-4 md:p-6">
      <div className="flex items-center justify-between mb-4">
        <h2 className="text-xl font-semibold">Operaciones</h2>
        {account ? (
          <span className="text-sm text-gray-600">
            {account.number} · Saldo <b>{account.balance} {account.currency}</b>
          </span>
        ) : (
          <span className="text-sm text-gray-500">Selecciona una cuenta</span>
        )}
      </div>

      <div className="flex gap-2 mb-4">
        <button
          onClick={() => setTab("deposit")}
          className={`px-3 py-2 rounded ${
            tab === "deposit" ? "bg-blue-600 text-white" : "bg-gray-200"
          }`}
        >
          Depositar
        </button>
        <button
          onClick={() => setTab("withdraw")}
          className={`px-3 py-2 rounded ${
            tab === "withdraw" ? "bg-blue-600 text-white" : "bg-gray-200"
          }`}
        >
          Retirar
        </button>
        <button
          onClick={() => setTab("transfer")}
          className={`px-3 py-2 rounded ${
            tab === "transfer" ? "bg-blue-600 text-white" : "bg-gray-200"
          }`}
        >
          Transferir
        </button>
      </div>

      {/* Monto */}
      <div className="space-y-3">
        <label className="block text-sm text-gray-600">Monto</label>
        <input
          type="number"
          step="0.01"
          className="border w-full p-2 rounded text-gray-800"
          value={amount}
          onChange={(e) => setAmount(e.target.value)}
          disabled={!canOperate || busy}
        />

        {tab === "deposit" && (
          <button
            onClick={doDeposit}
            disabled={!canOperate || busy || !amount}
            className="bg-emerald-600 text-white px-4 py-2 rounded hover:bg-emerald-700 disabled:opacity-50"
          >
            Confirmar depósito
          </button>
        )}

        {tab === "withdraw" && (
          <button
            onClick={doWithdraw}
            disabled={!canOperate || busy || !amount}
            className="bg-orange-600 text-white px-4 py-2 rounded hover:bg-orange-700 disabled:opacity-50"
          >
            Confirmar retiro
          </button>
        )}

        {tab === "transfer" && (
          <div className="p-3 rounded border border-dashed text-sm text-gray-600">
            Placeholder de transferencia (UI lista).  
            Para hacerlo bien, haremos un endpoint transaccional que debite y acredite
            en una sola operación (ACID
          </div>
        )}

        {msg && <p className="text-sm text-gray-700">{msg}</p>}
      </div>
    </div>
  );
}
