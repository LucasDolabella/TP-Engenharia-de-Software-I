const Jogos = {
  _buscarTimer: null,

  async carregar() {
    const busca = document.getElementById("busca-input").value;
    const lista = document.getElementById("jogos-lista");
    lista.innerHTML = "<p style='color:#718096;padding:1rem'>Carregando...</p>";
    const jogos = await Api.get(`/jogos${busca ? "?busca=" + encodeURIComponent(busca) : ""}`);
    if (jogos.length === 0) {
      lista.innerHTML = `<div class="empty-state"><div class="icon">🎲</div><p>Nenhum jogo encontrado.</p></div>`;
      return;
    }
    const usuario = JSON.parse(localStorage.getItem("usuario") || "{}");
    lista.innerHTML = jogos.map(j => `
      <div class="jogo-card">
        <h3>${j.nome}</h3>
        <span class="categoria">${j.categoria}</span>
        <p class="descricao">${j.descricao}</p>
        <p class="dono">👤 ${j.dono_nome}</p>
        <span class="status-badge status-${j.status}">${j.status === "DISPONIVEL" ? "Disponível" : "Emprestado"}</span>
        <div class="card-actions">
          ${j.status === "DISPONIVEL" && j.dono_id !== usuario.id
            ? `<button class="btn-primary btn-sm" onclick="Jogos.solicitarEmprestimo('${j.id}', '${j.nome}')">Pegar Emprestado</button>`
            : ""}
        </div>
      </div>
    `).join("");
  },

  buscar() {
    clearTimeout(this._buscarTimer);
    this._buscarTimer = setTimeout(() => this.carregar(), 300);
  },

  solicitarEmprestimo(jogoId, jogoNome) {
    const usuario = JSON.parse(localStorage.getItem("usuario") || "{}");
    if (usuario.status === "BLOQUEADO") {
      alert("Sua conta está bloqueada. Pague a penalidade pendente para solicitar empréstimos.");
      return;
    }
    document.getElementById("modal-jogo-id").value = jogoId;
    document.getElementById("modal-jogo-nome").textContent = `Jogo: ${jogoNome}`;
    const amanha = new Date();
    amanha.setDate(amanha.getDate() + 1);
    document.getElementById("modal-data-prazo").min = amanha.toISOString().split("T")[0];
    App.abrirModal("modal-emprestimo");
  },

  async confirmarEmprestimo(e) {
    e.preventDefault();
    const jogoId = document.getElementById("modal-jogo-id").value;
    const dataPrazo = document.getElementById("modal-data-prazo").value + "T23:59:59";
    const res = await Api.post("/emprestimos", { jogo_id: jogoId, data_prazo: dataPrazo });
    if (res.erro) {
      alert("Erro: " + res.erro);
    } else {
      App.fecharModal();
      alert("Empréstimo solicitado com sucesso!");
      this.carregar();
    }
  },
};

const MeusJogos = {
  _editandoId: null,

  async carregar() {
    const lista = document.getElementById("meus-jogos-lista");
    lista.innerHTML = "<p style='color:#718096;padding:1rem'>Carregando...</p>";
    const jogos = await Api.get("/jogos/meus");
    if (jogos.length === 0) {
      lista.innerHTML = `<div class="empty-state"><div class="icon">🎮</div><p>Você ainda não cadastrou nenhum jogo.</p></div>`;
      return;
    }
    lista.innerHTML = jogos.map(j => `
      <div class="jogo-card">
        <h3>${j.nome}</h3>
        <span class="categoria">${j.categoria}</span>
        <p class="descricao">${j.descricao}</p>
        <span class="status-badge status-${j.status}">${j.status === "DISPONIVEL" ? "Disponível" : "Emprestado"}</span>
        <div class="card-actions">
          <button class="btn-secondary btn-sm" onclick="MeusJogos.editar('${j.id}', '${j.nome.replace(/'/g,"\\'")}', '${j.categoria}', \`${j.descricao.replace(/`/g,"\\`")}\`)">Editar</button>
          <button class="btn-danger btn-sm" onclick="MeusJogos.remover('${j.id}')">Remover</button>
        </div>
      </div>
    `).join("");
  },

  mostrarForm() {
    this._editandoId = null;
    document.getElementById("form-jogo-titulo").textContent = "Novo Jogo";
    document.getElementById("jogo-edit-id").value = "";
    document.getElementById("jogo-nome").value = "";
    document.getElementById("jogo-categoria").value = "";
    document.getElementById("jogo-descricao").value = "";
    document.getElementById("form-jogo-container").classList.remove("hidden");
  },

  cancelar() {
    document.getElementById("form-jogo-container").classList.add("hidden");
    this._editandoId = null;
  },

  editar(id, nome, categoria, descricao) {
    this._editandoId = id;
    document.getElementById("form-jogo-titulo").textContent = "Editar Jogo";
    document.getElementById("jogo-edit-id").value = id;
    document.getElementById("jogo-nome").value = nome;
    document.getElementById("jogo-categoria").value = categoria;
    document.getElementById("jogo-descricao").value = descricao;
    document.getElementById("form-jogo-container").classList.remove("hidden");
    document.getElementById("form-jogo-container").scrollIntoView({ behavior: "smooth" });
  },

  async salvar(e) {
    e.preventDefault();
    const nome = document.getElementById("jogo-nome").value;
    const categoria = document.getElementById("jogo-categoria").value;
    const descricao = document.getElementById("jogo-descricao").value;
    let res;
    if (this._editandoId) {
      res = await Api.put(`/jogos/${this._editandoId}`, { nome, categoria, descricao });
    } else {
      res = await Api.post("/jogos", { nome, descricao, categoria });
    }
    if (res.erro) {
      alert("Erro: " + res.erro);
    } else {
      this.cancelar();
      this.carregar();
    }
  },

  async remover(id) {
    if (!confirm("Tem certeza que deseja remover este jogo?")) return;
    const res = await Api.delete(`/jogos/${id}`);
    if (res.erro) alert("Erro: " + res.erro);
    else this.carregar();
  },
};