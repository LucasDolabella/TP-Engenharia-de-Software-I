"""
Testes de Integração – Joga Aí
Testam os fluxos completos via API REST, cobrindo os cenários
definidos nos Casos de Uso da Sprint 2.
"""
import pytest
import json
from datetime import datetime, timedelta


# ── HELPERS ───────────────────────────────────────────────────────────────────

def registrar(client, nome, email, senha="senha123"):
    r = client.post("/api/auth/cadastrar", json={"nome": nome, "email": email, "senha": senha})
    data = json.loads(r.data)
    return data.get("token"), data.get("usuario")


def header(token):
    return {"Authorization": f"Bearer {token}"}


def criar_jogo(client, token, nome="Catan", categoria="Estratégia"):
    r = client.post("/api/jogos", json={
        "nome": nome,
        "descricao": "Jogo de estratégia com recursos",
        "categoria": categoria,
    }, headers=header(token))
    return json.loads(r.data)


def solicitar_emprestimo(client, token, jogo_id, dias=7):
    prazo = (datetime.utcnow() + timedelta(days=dias)).strftime("%Y-%m-%dT23:59:59")
    r = client.post("/api/emprestimos", json={"jogo_id": jogo_id, "data_prazo": prazo}, headers=header(token))
    return r, json.loads(r.data)


def solicitar_emprestimo_atrasado(client, token, jogo_id, dias_atras=3):
    prazo = (datetime.utcnow() - timedelta(days=dias_atras)).strftime("%Y-%m-%dT23:59:59")
    r = client.post("/api/emprestimos", json={"jogo_id": jogo_id, "data_prazo": prazo}, headers=header(token))
    return r, json.loads(r.data)


# ── CENÁRIO 1: AUTENTICAÇÃO ───────────────────────────────────────────────────

class TestAutenticacao:

    def test_cadastro_retorna_token(self, client):
        r = client.post("/api/auth/cadastrar", json={
            "nome": "Lucas", "email": "lucas@test.com", "senha": "senha123"
        })
        data = json.loads(r.data)
        assert r.status_code == 201
        assert "token" in data
        assert data["usuario"]["status"] == "ATIVO"

    def test_cadastro_email_duplicado_retorna_409(self, client):
        client.post("/api/auth/cadastrar", json={"nome": "A", "email": "dup@test.com", "senha": "123"})
        r = client.post("/api/auth/cadastrar", json={"nome": "B", "email": "dup@test.com", "senha": "123"})
        assert r.status_code == 409

    def test_login_credenciais_corretas(self, client):
        registrar(client, "Lucas", "lucas@test.com")
        r = client.post("/api/auth/login", json={"email": "lucas@test.com", "senha": "senha123"})
        assert r.status_code == 200
        assert "token" in json.loads(r.data)

    def test_login_senha_errada_retorna_401(self, client):
        registrar(client, "Lucas", "lucas@test.com")
        r = client.post("/api/auth/login", json={"email": "lucas@test.com", "senha": "errada"})
        assert r.status_code == 401

    def test_rota_protegida_sem_token_retorna_401(self, client):
        r = client.get("/api/jogos/meus")
        assert r.status_code == 401

    def test_perfil_retorna_dados_do_usuario(self, client):
        token, _ = registrar(client, "Lucas", "lucas@test.com")
        r = client.get("/api/auth/perfil", headers=header(token))
        data = json.loads(r.data)
        assert r.status_code == 200
        assert data["email"] == "lucas@test.com"
        assert "senha" not in data


# ── CENÁRIO 2: GERENCIAMENTO DE JOGOS ────────────────────────────────────────

class TestJogos:

    def test_cadastrar_jogo(self, client):
        token, _ = registrar(client, "Dono", "dono@test.com")
        jogo = criar_jogo(client, token)
        assert jogo["nome"] == "Catan"
        assert jogo["status"] == "DISPONIVEL"

    def test_listar_jogos_sem_autenticacao(self, client):
        token, _ = registrar(client, "Dono", "dono@test.com")
        criar_jogo(client, token)
        r = client.get("/api/jogos")
        assert r.status_code == 200
        assert len(json.loads(r.data)) == 1

    def test_buscar_jogo_por_nome(self, client):
        token, _ = registrar(client, "Dono", "dono@test.com")
        criar_jogo(client, token, nome="Pandemic")
        criar_jogo(client, token, nome="Catan")
        r = client.get("/api/jogos?busca=Pandemic")
        jogos = json.loads(r.data)
        assert len(jogos) == 1
        assert jogos[0]["nome"] == "Pandemic"

    def test_buscar_jogo_por_categoria(self, client):
        token, _ = registrar(client, "Dono", "dono@test.com")
        criar_jogo(client, token, nome="Dixit", categoria="Party")
        criar_jogo(client, token, nome="Catan", categoria="Estratégia")
        r = client.get("/api/jogos?busca=Party")
        jogos = json.loads(r.data)
        assert any(j["nome"] == "Dixit" for j in jogos)

    def test_remover_jogo_proprio(self, client):
        token, _ = registrar(client, "Dono", "dono@test.com")
        jogo = criar_jogo(client, token)
        r = client.delete(f"/api/jogos/{jogo['id']}", headers=header(token))
        assert r.status_code == 200

    def test_remover_jogo_alheio_retorna_erro(self, client):
        t1, _ = registrar(client, "Dono", "dono@test.com")
        t2, _ = registrar(client, "Outro", "outro@test.com")
        jogo = criar_jogo(client, t1)
        r = client.delete(f"/api/jogos/{jogo['id']}", headers=header(t2))
        assert r.status_code == 400

    def test_meus_jogos_retorna_apenas_do_usuario(self, client):
        t1, _ = registrar(client, "Dono", "dono@test.com")
        t2, _ = registrar(client, "Outro", "outro@test.com")
        criar_jogo(client, t1, nome="Catan")
        criar_jogo(client, t2, nome="Pandemic")
        r = client.get("/api/jogos/meus", headers=header(t1))
        jogos = json.loads(r.data)
        assert len(jogos) == 1
        assert jogos[0]["nome"] == "Catan"


# ── CENÁRIO 3: SOLICITAR EMPRÉSTIMO ──────────────────────────────────────────

class TestSolicitarEmprestimo:

    def test_solicitar_emprestimo_com_sucesso(self, client):
        t_dono, _ = registrar(client, "Dono", "dono@test.com")
        t_sol, _ = registrar(client, "Sol", "sol@test.com")
        jogo = criar_jogo(client, t_dono)
        r, data = solicitar_emprestimo(client, t_sol, jogo["id"])
        assert r.status_code == 201
        assert data["status"] == "ATIVO"

    def test_jogo_fica_indisponivel_apos_emprestimo(self, client):
        t_dono, _ = registrar(client, "Dono", "dono@test.com")
        t_sol, _ = registrar(client, "Sol", "sol@test.com")
        jogo = criar_jogo(client, t_dono)
        solicitar_emprestimo(client, t_sol, jogo["id"])
        r = client.get(f"/api/jogos/{jogo['id']}")
        assert json.loads(r.data)["status"] == "EMPRESTADO"

    def test_nao_pode_solicitar_proprio_jogo(self, client):
        token, _ = registrar(client, "Dono", "dono@test.com")
        jogo = criar_jogo(client, token)
        r, data = solicitar_emprestimo(client, token, jogo["id"])
        assert r.status_code == 400

    def test_nao_pode_solicitar_jogo_indisponivel(self, client):
        t_dono, _ = registrar(client, "Dono", "dono@test.com")
        t_sol1, _ = registrar(client, "Sol1", "sol1@test.com")
        t_sol2, _ = registrar(client, "Sol2", "sol2@test.com")
        jogo = criar_jogo(client, t_dono)
        solicitar_emprestimo(client, t_sol1, jogo["id"])
        r, data = solicitar_emprestimo(client, t_sol2, jogo["id"])
        assert r.status_code == 400

    def test_cancelar_emprestimo_libera_jogo(self, client):
        t_dono, _ = registrar(client, "Dono", "dono@test.com")
        t_sol, _ = registrar(client, "Sol", "sol@test.com")
        jogo = criar_jogo(client, t_dono)
        _, emp = solicitar_emprestimo(client, t_sol, jogo["id"])
        r = client.put(f"/api/emprestimos/{emp['id']}/cancelar", headers=header(t_sol))
        assert r.status_code == 200
        jogo_atualizado = json.loads(client.get(f"/api/jogos/{jogo['id']}").data)
        assert jogo_atualizado["status"] == "DISPONIVEL"


# ── CENÁRIO 4: CONFIRMAR DEVOLUÇÃO ───────────────────────────────────────────

class TestConfirmarDevolucao:

    def test_dono_confirma_devolucao(self, client):
        t_dono, _ = registrar(client, "Dono", "dono@test.com")
        t_sol, _ = registrar(client, "Sol", "sol@test.com")
        jogo = criar_jogo(client, t_dono)
        _, emp = solicitar_emprestimo(client, t_sol, jogo["id"])
        r = client.put(f"/api/emprestimos/{emp['id']}/confirmar-devolucao", headers=header(t_dono))
        data = json.loads(r.data)
        assert r.status_code == 200
        assert data["status"] == "DEVOLVIDO"

    def test_jogo_disponivel_apos_devolucao(self, client):
        t_dono, _ = registrar(client, "Dono", "dono@test.com")
        t_sol, _ = registrar(client, "Sol", "sol@test.com")
        jogo = criar_jogo(client, t_dono)
        _, emp = solicitar_emprestimo(client, t_sol, jogo["id"])
        client.put(f"/api/emprestimos/{emp['id']}/confirmar-devolucao", headers=header(t_dono))
        jogo_atualizado = json.loads(client.get(f"/api/jogos/{jogo['id']}").data)
        assert jogo_atualizado["status"] == "DISPONIVEL"

    def test_solicitante_nao_pode_confirmar_devolucao(self, client):
        t_dono, _ = registrar(client, "Dono", "dono@test.com")
        t_sol, _ = registrar(client, "Sol", "sol@test.com")
        jogo = criar_jogo(client, t_dono)
        _, emp = solicitar_emprestimo(client, t_sol, jogo["id"])
        r = client.put(f"/api/emprestimos/{emp['id']}/confirmar-devolucao", headers=header(t_sol))
        assert r.status_code == 400


# ── CENÁRIO 5: APLICAR PENALIDADE ────────────────────────────────────────────

class TestAplicarPenalidade:

    def test_nao_devolucao_bloqueia_solicitante(self, client):
        t_dono, _ = registrar(client, "Dono", "dono@test.com")
        t_sol, u_sol = registrar(client, "Sol", "sol@test.com")
        jogo = criar_jogo(client, t_dono)
        _, emp = solicitar_emprestimo_atrasado(client, t_sol, jogo["id"])
        client.put(f"/api/emprestimos/{emp['id']}/nao-devolvido", headers=header(t_dono))
        perfil = json.loads(client.get("/api/auth/perfil", headers=header(t_sol)).data)
        assert perfil["status"] == "BLOQUEADO"

    def test_usuario_bloqueado_nao_pode_solicitar(self, client):
        t_dono, _ = registrar(client, "Dono", "dono@test.com")
        t_sol, _ = registrar(client, "Sol", "sol@test.com")
        jogo1 = criar_jogo(client, t_dono, nome="Catan")
        _, emp = solicitar_emprestimo_atrasado(client, t_sol, jogo1["id"])
        client.put(f"/api/emprestimos/{emp['id']}/nao-devolvido", headers=header(t_dono))
        jogo2 = criar_jogo(client, t_dono, nome="Pandemic")
        r, data = solicitar_emprestimo(client, t_sol, jogo2["id"])
        assert r.status_code == 400
        assert "bloqueado" in data.get("erro", "").lower()

    def test_penalidade_criada_com_valor_correto(self, client):
        t_dono, _ = registrar(client, "Dono", "dono@test.com")
        t_sol, _ = registrar(client, "Sol", "sol@test.com")
        jogo = criar_jogo(client, t_dono)
        # usa 5 dias para garantir pelo menos 4 dias completos no cálculo de atraso
        _, emp = solicitar_emprestimo_atrasado(client, t_sol, jogo["id"], dias_atras=5)
        client.put(f"/api/emprestimos/{emp['id']}/nao-devolvido", headers=header(t_dono))
        pens = json.loads(client.get("/api/penalidades", headers=header(t_sol)).data)
        assert len(pens) == 1
        assert pens[0]["valor_multa"] >= 4 * 5.0
        assert pens[0]["status"] == "PENDENTE"


# ── CENÁRIO 6: PAGAMENTO DE MULTA ────────────────────────────────────────────

class TestPagamentoMulta:

    def _setup_penalidade(self, client):
        t_dono, _ = registrar(client, "Dono", "dono@test.com")
        t_sol, _ = registrar(client, "Sol", "sol@test.com")
        jogo = criar_jogo(client, t_dono)
        _, emp = solicitar_emprestimo_atrasado(client, t_sol, jogo["id"])
        client.put(f"/api/emprestimos/{emp['id']}/nao-devolvido", headers=header(t_dono))
        pens = json.loads(client.get("/api/penalidades", headers=header(t_sol)).data)
        return t_sol, pens[0]["id"]

    def test_pagar_multa_desbloqueia_usuario(self, client):
        t_sol, pen_id = self._setup_penalidade(client)
        client.post(f"/api/penalidades/{pen_id}/pagar", json={"metodo": "cartao"}, headers=header(t_sol))
        perfil = json.loads(client.get("/api/auth/perfil", headers=header(t_sol)).data)
        assert perfil["status"] == "ATIVO"

    def test_pagar_multa_marca_penalidade_como_paga(self, client):
        t_sol, pen_id = self._setup_penalidade(client)
        client.post(f"/api/penalidades/{pen_id}/pagar", json={"metodo": "cartao"}, headers=header(t_sol))
        pens = json.loads(client.get("/api/penalidades", headers=header(t_sol)).data)
        assert pens[0]["status"] == "PAGA"

    def test_outro_usuario_nao_pode_pagar_multa_alheia(self, client):
        t_sol, pen_id = self._setup_penalidade(client)
        t_outro, _ = registrar(client, "Outro", "outro@test.com")
        r = client.post(f"/api/penalidades/{pen_id}/pagar", json={"metodo": "cartao"}, headers=header(t_outro))
        assert r.status_code == 400


# ── CENÁRIO 7: CHAT ───────────────────────────────────────────────────────────

class TestChat:

    def test_enviar_mensagem_no_chat(self, client):
        t_dono, _ = registrar(client, "Dono", "dono@test.com")
        t_sol, _ = registrar(client, "Sol", "sol@test.com")
        jogo = criar_jogo(client, t_dono)
        _, emp = solicitar_emprestimo(client, t_sol, jogo["id"])
        r = client.post(f"/api/chat/{emp['id']}", json={"conteudo": "Olá!"}, headers=header(t_sol))
        assert r.status_code == 201

    def test_listar_mensagens_do_chat(self, client):
        t_dono, _ = registrar(client, "Dono", "dono@test.com")
        t_sol, _ = registrar(client, "Sol", "sol@test.com")
        jogo = criar_jogo(client, t_dono)
        _, emp = solicitar_emprestimo(client, t_sol, jogo["id"])
        client.post(f"/api/chat/{emp['id']}", json={"conteudo": "Olá!"}, headers=header(t_sol))
        client.post(f"/api/chat/{emp['id']}", json={"conteudo": "Tudo bem?"}, headers=header(t_dono))
        r = client.get(f"/api/chat/{emp['id']}", headers=header(t_sol))
        msgs = json.loads(r.data)
        assert len(msgs) == 2

    def test_mensagem_vazia_retorna_erro(self, client):
        t_dono, _ = registrar(client, "Dono", "dono@test.com")
        t_sol, _ = registrar(client, "Sol", "sol@test.com")
        jogo = criar_jogo(client, t_dono)
        _, emp = solicitar_emprestimo(client, t_sol, jogo["id"])
        r = client.post(f"/api/chat/{emp['id']}", json={"conteudo": "  "}, headers=header(t_sol))
        assert r.status_code == 400

    def test_terceiro_nao_pode_acessar_chat(self, client):
        t_dono, _ = registrar(client, "Dono", "dono@test.com")
        t_sol, _ = registrar(client, "Sol", "sol@test.com")
        t_outro, _ = registrar(client, "Outro", "outro@test.com")
        jogo = criar_jogo(client, t_dono)
        _, emp = solicitar_emprestimo(client, t_sol, jogo["id"])
        r = client.get(f"/api/chat/{emp['id']}", headers=header(t_outro))
        assert r.status_code == 400