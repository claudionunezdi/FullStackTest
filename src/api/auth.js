import API from "./api";

export const login = ({ username, password }) =>
  API.post("/auth/login/", { username, password });

export const refresh = (refreshToken) =>
  API.post("/auth/refresh/", { refresh: refreshToken });

export const register = (data) => API.post("/auth/register/", data);
