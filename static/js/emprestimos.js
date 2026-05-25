const Emprestimos = {
  async carregar() {
    const lista = document.getElementById("emprestimos-lista");
    lista.innerHTML = "<p style='color:#718096;padding:1rem'>Carregando...</p>";
    const emprestimos = await Api.get("/emprestimos");
    const usuario = JSON.parse(localStorage.getItem("usuario") || "{}");
    if (emprestimos.length === 0) {
      lista.innerHTML = `<div class="empty-state"><div class="icon">📦</div><p>Nenhum empréstimo encontrado.</p></div>`;
      return;
    }
    lista.innerHTML = emprestimos.map(e => {
      const isSolicitante = e.solicitante_id === usuario.id;
      const isDono = e.dono_id === usuario.id;
      const prazo = new Date(e.data_prazo).toLocaleDateString("pt-BR");
      const inicio = new Date(e.data_inicio).toLocaleDateString("pt-BR");
      const papel = isSolicitante ? "📤 Você pegou emprestado" : "📥 Você emprestou";

      let acoes = "";
      if (e.status === "ATIVO") {
        acoes += `<button class="btn-secondary btn-sm" onclick="Chat.abrir('${e.id}', '${e.jogo_nome}')">💬 Chat</button>`;
        if (isDono) {
          acoes += `<button class="btn-primary btn-sm" onclick="Emprestimos.confirmarDevolucao('${e.id}')">✅ Confirmar Devolução</button>`;
          acoes += `<button class="btn-danger btn-sm" onclick="Emprestimos.naoDevolucao('${e.id}')">⚠️ Não Devolvido</button>`;
        }
        if (isSolicitante) {
          acoes += `<button class="btn-danger btn-sm" onclick="Emprestimos.cancelar('${e.id}')">Cancelar</button>`;
        }
      }

      return `
        <div class="emprestimo-card">
          <div style="display:flex;justify-content:space-between;align-items:flex-start">
            <div>
              <h3>🎲 ${e.jogo_nome}</h3>
              <p class="emprestimo-meta">${papel}</p>
              <p class="emprestimo-meta">De: <b>${e.dono_nome}</b> → Para: <b>${e.solicitante_nome}</b></p>
              <p class="emprestimo-meta">Início: ${inicio} | Prazo: ${prazo}</p>
              ${e.em_atraso ? `<span class="atraso-badge">⏰ ${e.dias_atraso} dia(s) de atraso</span>` : ""}
            </div>
            <span class="status-badge status-${e.status}">${e.status}</span>
          </div>
          <div class="card-actions" style="margin-top:0.8rem">${acoes}</div>
        </div>
      `;
    }).join("");
  },

  async confirmarDevolucao(id) {
    if (!confirm("Confirmar que o jogo foi devolvido?")) return;
    const res = await Api.put(`/emprestimos/${id}/confirmar-devolucao`);
    if (res.erro) alert("Erro: " + res.erro);
    else { alert("Devolução confirmada!"); this.carregar(); }
  },

  async naoDevolucao(id) {
    if (!confirm("Registrar que o jogo NÃO foi devolvido? Uma multa será aplicada ao solicitante.")) return;
    const res = await Api.put(`/emprestimos/${id}/nao-devolvido`);
    if (res.erro) alert("Erro: " + res.erro);
    else { alert("Não devolução registrada. Penalidade aplicada ao solicitante."); this.carregar(); }
  },

  async cancelar(id) {
    if (!confirm("Cancelar este empréstimo?")) return;
    const res = await Api.put(`/emprestimos/${id}/cancelar`);
    if (res.erro) alert("Erro: " + res.erro);
    else { alert("Empréstimo cancelado."); this.carregar(); }
  },
};

const Penalidades = {
  async carregar() {
    const lista = document.getElementById("penalidades-lista");
    lista.innerHTML = "<p style='color:#718096;padding:1rem'>Carregando...</p>";
    const penalidades = await Api.get("/penalidades");
    if (penalidades.length === 0) {
      lista.innerHTML = `<div class="empty-state"><div class="icon">✅</div><p>Nenhuma penalidade. Você está em dia!</p></div>`;
      return;
    }
    lista.innerHTML = penalidades.map(p => `
      <div class="penalidade-card">
        <h3>⚠️ Penalidade${p.jogo_nome ? " – " + p.jogo_nome : ""}</h3>
        <div class="penalidade-valor">R$ ${p.valor_multa.toFixed(2)}</div>
        <p class="emprestimo-meta">Aplicada em: ${new Date(p.data_aplicacao).toLocaleDateString("pt-BR")}</p>
        <span class="status-badge status-${p.status}">${p.status}</span>
        ${p.status === "PENDENTE" ? `
          <div class="card-actions" style="margin-top:1rem">
            <button class="btn-primary btn-sm" onclick="Penalidades.pagar('${p.id}')">💳 Pagar Multa</button>
          </div>` : ""}
      </div>
    `).join("");
  },

  async pagar(id) {
    if (!confirm("Confirmar pagamento da multa?")) return;
    const res = await Api.post(`/penalidades/${id}/pagar`, { metodo: "cartao" });
    if (res.sucesso) {
      alert(res.mensagem);
      const perfilRes = await Api.get("/auth/perfil");
      localStorage.setItem("usuario", JSON.stringify(perfilRes));
      this.carregar();
    } else {
      alert("Erro: " + res.mensagem);
    }
  },
};

const Notificacoes = {
  async carregar() {
    const lista = document.getElementById("notificacoes-lista");
    lista.innerHTML = "<p style='color:#718096;padding:1rem'>Carregando...</p>";
    const notifs = await Api.get("/notificacoes");
    if (notifs.length === 0) {
      lista.innerHTML = `<div class="empty-state"><div class="icon">🔔</div><p>Nenhuma notificação.</p></div>`;
      return;
    }
    const icones = {
      SOLICITACAO_EMPRESTIMO: "📨",
      PRAZO_VENCIDO: "⏰",
      DEVOLUCAO_CONFIRMADA: "✅",
      NOVA_MENSAGEM: "💬",
      PENALIDADE_APLICADA: "⚠️",
    };
    lista.innerHTML = notifs.map(n => `
      <div class="notif-item ${n.lida ? "" : "notif-nao-lida"}">
        <div class="notif-icon">${icones[n.tipo] || "🔔"}</div>
        <div>
          <div>${n.mensagem}</div>
          <div class="notif-hora">${new Date(n.data_envio).toLocaleString("pt-BR")}</div>
        </div>
      </div>
    `).join("");
  },

  async marcarTodasLidas() {
    await Api.put("/notificacoes/marcar-todas-lidas");
    this.carregar();
    App.atualizarBadgeNotificacoes();
  },
};