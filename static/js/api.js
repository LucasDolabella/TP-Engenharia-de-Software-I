const API_BASE = "/api";

const Api = {
  token: localStorage.getItem("token"),

  setToken(token) {
    this.token = token;
    if (token) localStorage.setItem("token", token);
    else localStorage.removeItem("token");
  },

  headers() {
    const h = { "Content-Type": "application/json" };
    if (this.token) h["Authorization"] = `Bearer ${this.token}`;
    return h;
  },

  async get(path) {
    const res = await fetch(API_BASE + path, { headers: this.headers() });
    return res.json();
  },

  async post(path, body) {
    const res = await fetch(API_BASE + path, {
      method: "POST",
      headers: this.headers(),
      body: JSON.stringify(body),
    });
    return res.json();
  },

  async put(path, body = {}) {
    const res = await fetch(API_BASE + path, {
      method: "PUT",
      headers: this.headers(),
      body: JSON.stringify(body),
    });
    return res.json();
  },

  async delete(path) {
    const res = await fetch(API_BASE + path, {
      method: "DELETE",
      headers: this.headers(),
    });
    return res.json();
  },
};