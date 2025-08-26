import { AuthProvider } from "./context/AuthProvider";
import LoginPage from "./pages/LoginPage";
import AppRouter from "./router/AppRouter";

function App() {
  return (
    <AuthProvider>
      <AppRouter />
      
    </AuthProvider>
  );
}

export default App;