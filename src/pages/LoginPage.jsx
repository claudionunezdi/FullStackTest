import LoginForm from "../components/forms/LoginForm";
export default function LoginPage() {
  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-100">
      <div className="w-full max-w-md bg-white shadow-md rounded-lg p-8">
        <h1 className="text-2xl font-bold text-center mb-6 text-gray-800">Iniciar Sesión</h1>
        <LoginForm />  {/* 👈 Aquí renderizamos tu formulario */}
      </div>
    </div>
  );
}