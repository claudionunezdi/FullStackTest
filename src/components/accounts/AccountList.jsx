export default function AccountList({ accounts, selectedId, onSelect }) {
    if (!accounts.length) {
        return <p className="text-gray-600">No tienes cuenta aún</p>;
    }
    return (
    <ul className="space-y-2">
      {accounts.map((acc) => {
        const active = acc.id === selectedId;
        return (
          <li
            key={acc.id}
            className={`p-3 border rounded cursor-pointer ${
              active ? "bg-blue-50 border-blue-300" : "bg-white hover:bg-gray-50"
            }`}
            onClick={() => onSelect?.(acc)}
          >
            <div className="flex justify-between">
              <div className="font-medium">{acc.number}</div>
              <div className="text-sm text-gray-500">{acc.currency}</div>
            </div>
            <div className="text-sm text-gray-700">
              Saldo: <span className="font-semibold">{acc.balance}</span>
            </div>
          </li>
        );
      })}
    </ul>
  );
}