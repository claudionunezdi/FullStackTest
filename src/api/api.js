import axios from "axios";

const API = axios.create({
  baseURL: "http://127.0.0.1:8000/api",
});

// Adjunta el access token en cada request
API.interceptors.request.use((config) => {
  const access = localStorage.getItem("access");
  if (access) config.headers.Authorization = `Bearer ${access}`;
  return config;
});

// Si el access expiró (401), intenta refrescar y reintenta la request
let isRefreshing = false;
let queue = [];

API.interceptors.request.use((config) => {
  const token = localStorage.getItem("token");
  if (token) config.headers.Authorization = `Bearer ${token}`;

  // Si es escritura y no termina en slash (y no hay query), agrega '/'
  const needsSlash =
    ["post", "put", "patch", "delete"].includes((config.method || "").toLowerCase()) &&
    typeof config.url === "string" &&
    !config.url.endsWith("/") &&
    !config.url.includes("?");

  if (needsSlash) config.url += "/";

  return config;
});



API.interceptors.response.use(
  (res) => res,
  async (error) => {
    const original = error.config;

    // Si no es 401 o ya intentamos refrescar esta misma request, rechaza
    if (error.response?.status !== 401 || original._retry) {
      return Promise.reject(error);
    }

    // Marca para no reintentar en bucle
    original._retry = true;

    const refresh = localStorage.getItem("refresh");
    if (!refresh) return Promise.reject(error);

    // Cola para evitar múltiples refresh simultáneos
    if (isRefreshing) {
      return new Promise((resolve, reject) => {
        queue.push({ resolve, reject });
      })
        .then((token) => {
          original.headers.Authorization = `Bearer ${token}`;
          return API(original);
        })
        .catch(Promise.reject);
    }

    try {
      isRefreshing = true;
      const r = await axios.post("http://127.0.0.1:8000/api/auth/refresh/", { refresh });
      const newAccess = r.data.access;
      localStorage.setItem("access", newAccess);

      // Despierta la cola
      queue.forEach((p) => p.resolve(newAccess));
      queue = [];
      isRefreshing = false;

      // Reintenta la original con el nuevo token
      original.headers.Authorization = `Bearer ${newAccess}`;
      return API(original);
    } catch (e) {
      queue.forEach((p) => p.reject(e));
      queue = [];
      isRefreshing = false;

      // Borra tokens inválidos
      localStorage.removeItem("access");
      localStorage.removeItem("refresh");

      return Promise.reject(e);
    }
  }
);

export default API;
