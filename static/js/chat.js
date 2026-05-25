const Chat = {
  _emprestimoId: null,
  _intervalId: null,

  abrir(emprestimoId, jogoNome) {
    this._emprestimoId = emprestimoId;
    document.getElementById("chat-titulo").textContent = `Chat – ${jogoNome}`;
    document.getElementById("chat-conteudo").value = "";
    App.mostrarView("chat");
    this.carregar();
    clearInterval(this._intervalId);
    this._intervalId = setInterval(() => this.carregar(), 4000);
  },

  sair() {
    clearInterval(this._intervalId);
    this._emprestimoId = null;
  },

  async carregar() {
    if (!this._emprestimoId) return;
    const mensagens = await Api.get(`/chat/${this._emprestimoId}`);
    if (mensagens.erro) return;
    const usuario = JSON.parse(localStorage.getItem("usuario") || "{}");
    const container = document.getElementById("chat-mensagens");
    const estaNoFundo = container.scrollHeight - container.scrollTop === container.clientHeight;
    container.innerHTML = mensagens.length === 0
      ? `<div class="empty-state" style="margin:auto"><p>Sem mensagens ainda. Diga olá! 👋</p></div>`
      : mensagens.map(m => {
          const meu = m.remetente_id === usuario.id;
          const hora = new Date(m.data_envio).toLocaleTimeString("pt-BR", { hour: "2-digit", minute: "2-digit" });
          return `
            <div style="display:flex;flex-direction:column;align-items:${meu ? "flex-end" : "flex-start"}">
              ${!meu ? `<div class="msg-nome">${m.remetente_nome}</div>` : ""}
              <div class="msg-bubble ${meu ? "msg-meu" : "msg-outro"}">
                ${m.conteudo}
                <div class="msg-hora">${hora}</div>
              </div>
            </div>
          `;
        }).join("");
    if (estaNoFundo || mensagens.length > 0) {
      container.scrollTop = container.scrollHeight;
    }
  },

  async enviar(e) {
    e.preventDefault();
    const input = document.getElementById("chat-conteudo");
    const conteudo = input.value.trim();
    if (!conteudo || !this._emprestimoId) return;
    input.value = "";
    const res = await Api.post(`/chat/${this._emprestimoId}`, { conteudo });
    if (res.erro) {
      alert("Erro: " + res.erro);
      input.value = conteudo;
    } else {
      this.carregar();
    }
  },
};