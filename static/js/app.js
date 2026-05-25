const App = {
  _viewAtual: null,

  init() {
    const token = localStorage.getItem("token");
    const usuarioStr = localStorage.getItem("usuario");
    if (token && usuarioStr) {
      this.iniciarSessao(JSON.parse(usuarioStr));
    } else {
      this.mostrarView("auth");
    }
  },

  iniciarSessao(usuario) {
    document.getElementById("navbar").classList.remove("hidden");
    document.getElementById("nav-usuario").textContent = `👤 ${usuario.nome}`;
    if (usuario.status === "BLOQUEADO") {
      document.getElementById("nav-usuario").textContent += " 🔒";
    }
    this.mostrarView("jogos");
    this.atualizarBadgeNotificacoes();
    setInterval(() => this.atualizarBadgeNotificacoes(), 30000);
  },

  async atualizarBadgeNotificacoes() {
    const notifs = await Api.get("/notificacoes");
    if (notifs.erro) return;
    const naoLidas = notifs.filter(n => !n.lida).length;
    const badge = document.getElementById("notif-badge");
    if (naoLidas > 0) {
      badge.textContent = naoLidas;
      badge.classList.remove("hidden");
    } else {
      badge.classList.add("hidden");
    }
  },

  mostrarView(nome) {
    if (this._viewAtual === "chat" && nome !== "chat") {
      Chat.sair();
    }
    document.querySelectorAll(".view").forEach(v => v.classList.add("hidden"));
    const view = document.getElementById(`view-${nome}`);
    if (view) {
      view.classList.remove("hidden");
      this._viewAtual = nome;
    }
    switch (nome) {
      case "jogos":         Jogos.carregar(); break;
      case "meus-jogos":   MeusJogos.carregar(); break;
      case "emprestimos":  Emprestimos.carregar(); break;
      case "penalidades":  Penalidades.carregar(); break;
      case "notificacoes": Notificacoes.carregar(); this.atualizarBadgeNotificacoes(); break;
    }
  },

  logout() {
    Api.setToken(null);
    localStorage.removeItem("usuario");
    document.getElementById("navbar").classList.add("hidden");
    this.mostrarView("auth");
  },

  abrirModal(id) {
    document.getElementById(id).classList.remove("hidden");
    document.getElementById("modal-overlay").classList.remove("hidden");
  },

  fecharModal() {
    document.querySelectorAll(".modal").forEach(m => m.classList.add("hidden"));
    document.getElementById("modal-overlay").classList.add("hidden");
  },
};

document.addEventListener("DOMContentLoaded", () => App.init());