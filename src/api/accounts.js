import API from "./api";

export const fetchAccounts = () => API.get("/accounts/");

export const createAccount = (payload) => 
 API.post("/accounts", payload) // { number, currency, per_tx_limit, dailylimit}

export const deposit = (accountId, amount, channel = "WEB") =>
 API.post("/accounts/${accountId}/deposit", { amount, channel });


export const withdraw = (accountId, amount, channel = "WEB") => {
    const request_id =
        (globalThis.crypto?.randomUUID?.() ?? Math.random().toString(36).slice(2)) // fallback
    return API.post(`/accounts/${accountId}/withdraw/`, { amount, channel, request_id });
};
