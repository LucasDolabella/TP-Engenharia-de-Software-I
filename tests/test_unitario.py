"""
Testes Unitários – Joga Aí
Testam as regras de negócio das classes isoladamente,
sem depender de rotas HTTP ou banco de dados real.
"""
import pytest
from datetime import datetime, timedelta
from app.models.usuario import Usuario, StatusUsuario
from app.models.jogo import Jogo, StatusJogo
from app.models.emprestimo import Emprestimo, StatusEmprestimo
from app.models.penalidade import Penalidade, StatusPenalidade, MULTA_POR_DIA
from app.models.mensagem import Mensagem


# ── USUARIO ───────────────────────────────────────────────────────────────────

class TestUsuario:

    def test_cadastrar_define_status_ativo(self, app):
        u = Usuario()
        u.cadastrar("Lucas", "lucas@test.com", "senha123")
        assert u.status == StatusUsuario.ATIVO.value

    def test_senha_e_armazenada_como_hash(self, app):
        u = Usuario()
        u.cadastrar("Lucas", "lucas@test.com", "senha123")
        assert u.senha != "senha123"

    def test_validar_senha_correta(self, app):
        u = Usuario()
        u.cadastrar("Lucas", "lucas@test.com", "senha123")
        assert u._validar_senha("senha123") is True

    def test_validar_senha_incorreta(self, app):
        u = Usuario()
        u.cadastrar("Lucas", "lucas@test.com", "senha123")
        assert u._validar_senha("errada") is False

    def test_bloquear_muda_status(self, app, db):
        u = Usuario()
        u.cadastrar("Lucas", "lucas@test.com", "senha123")
        db.session.add(u)
        db.session.commit()
        u.bloquear()
        assert u.status == StatusUsuario.BLOQUEADO.value

    def test_desbloquear_muda_status(self, app, db):
        u = Usuario()
        u.cadastrar("Lucas", "lucas@test.com", "senha123")
        db.session.add(u)
        db.session.commit()
        u.bloquear()
        u.desbloquear()
        assert u.status == StatusUsuario.ATIVO.value

    def test_esta_bloqueado_retorna_true(self, app, db):
        u = Usuario()
        u.cadastrar("Lucas", "lucas@test.com", "senha123")
        db.session.add(u)
        db.session.commit()
        u.bloquear()
        assert u.esta_bloqueado() is True

    def test_esta_bloqueado_retorna_false_quando_ativo(self, app):
        u = Usuario()
        u.cadastrar("Lucas", "lucas@test.com", "senha123")
        assert u.esta_bloqueado() is False

    def test_atualizar_perfil_nome(self, app, db):
        u = Usuario()
        u.cadastrar("Lucas", "lucas@test.com", "senha123")
        db.session.add(u)
        db.session.commit()
        u.atualizar_perfil({"nome": "Lucas Atualizado"})
        assert u.nome == "Lucas Atualizado"

    def test_to_dict_nao_expoe_senha(self, app):
        u = Usuario()
        u.cadastrar("Lucas", "lucas@test.com", "senha123")
        d = u.to_dict()
        assert "senha" not in d
        assert d["email"] == "lucas@test.com"


# ── JOGO ──────────────────────────────────────────────────────────────────────

class TestJogo:

    def test_cadastrar_define_status_disponivel(self, app):
        j = Jogo()
        j.cadastrar("Catan", "Jogo de estratégia", "Estratégia")
        assert j.status == StatusJogo.DISPONIVEL.value

    def test_cadastrar_campos_obrigatorios_vazios_levanta_erro(self, app):
        j = Jogo()
        with pytest.raises(ValueError):
            j.cadastrar("", "", "")

    def test_verificar_disponibilidade_true(self, app):
        j = Jogo()
        j.cadastrar("Catan", "Descrição", "Estratégia")
        assert j.verificar_disponibilidade() is True

    def test_verificar_disponibilidade_false_quando_emprestado(self, app, db):
        j = Jogo()
        j.cadastrar("Catan", "Descrição", "Estratégia")
        j.dono_id = "qualquer-id"
        db.session.add(j)
        db.session.commit()
        j.atualizar_status(StatusJogo.EMPRESTADO.value)
        assert j.verificar_disponibilidade() is False

    def test_atualizar_nome_e_categoria(self, app):
        j = Jogo()
        j.cadastrar("Catan", "Descrição", "Estratégia")
        j.atualizar({"nome": "Catan Novo", "categoria": "Família"})
        assert j.nome == "Catan Novo"
        assert j.categoria == "Família"

    def test_to_dict_contem_campos_basicos(self, app):
        j = Jogo()
        j.cadastrar("Catan", "Descrição", "Estratégia")
        j.dono_id = "id-fake"
        d = j.to_dict()
        assert d["nome"] == "Catan"
        assert d["status"] == StatusJogo.DISPONIVEL.value


# ── EMPRESTIMO ────────────────────────────────────────────────────────────────

class TestEmprestimo:

    def _criar_usuario(self, db, nome, email):
        u = Usuario()
        u.cadastrar(nome, email, "senha123")
        db.session.add(u)
        db.session.commit()
        return u

    def _criar_jogo(self, db, nome, dono_id):
        j = Jogo()
        j.cadastrar(nome, "Descrição", "Estratégia")
        j.dono_id = dono_id
        db.session.add(j)
        db.session.commit()
        return j

    def test_solicitar_cria_emprestimo_ativo(self, app, db):
        dono = self._criar_usuario(db, "Dono", "dono@test.com")
        sol = self._criar_usuario(db, "Sol", "sol@test.com")
        jogo = self._criar_jogo(db, "Catan", dono.id)
        prazo = datetime.utcnow() + timedelta(days=7)

        e = Emprestimo()
        e.solicitar(sol, jogo, prazo)
        db.session.add(e)
        db.session.commit()

        assert e.status == StatusEmprestimo.ATIVO.value
        assert e.solicitante_id == sol.id

    def test_solicitar_usuario_bloqueado_levanta_erro(self, app, db):
        dono = self._criar_usuario(db, "Dono", "dono@test.com")
        sol = self._criar_usuario(db, "Sol", "sol@test.com")
        sol.bloquear()
        jogo = self._criar_jogo(db, "Catan", dono.id)
        prazo = datetime.utcnow() + timedelta(days=7)

        e = Emprestimo()
        with pytest.raises(ValueError, match="bloqueado"):
            e.solicitar(sol, jogo, prazo)

    def test_solicitar_jogo_indisponivel_levanta_erro(self, app, db):
        dono = self._criar_usuario(db, "Dono", "dono@test.com")
        sol = self._criar_usuario(db, "Sol", "sol@test.com")
        jogo = self._criar_jogo(db, "Catan", dono.id)
        jogo.atualizar_status(StatusJogo.EMPRESTADO.value)
        prazo = datetime.utcnow() + timedelta(days=7)

        e = Emprestimo()
        with pytest.raises(ValueError, match="disponível"):
            e.solicitar(sol, jogo, prazo)

    def test_solicitar_proprio_jogo_levanta_erro(self, app, db):
        dono = self._criar_usuario(db, "Dono", "dono@test.com")
        jogo = self._criar_jogo(db, "Catan", dono.id)
        prazo = datetime.utcnow() + timedelta(days=7)

        e = Emprestimo()
        with pytest.raises(ValueError, match="próprio"):
            e.solicitar(dono, jogo, prazo)

    def test_confirmar_devolucao_muda_status(self, app, db):
        dono = self._criar_usuario(db, "Dono", "dono@test.com")
        sol = self._criar_usuario(db, "Sol", "sol@test.com")
        jogo = self._criar_jogo(db, "Catan", dono.id)
        prazo = datetime.utcnow() + timedelta(days=7)

        e = Emprestimo()
        e.solicitar(sol, jogo, prazo)
        db.session.add(e)
        db.session.commit()
        e.confirmar_devolucao()

        assert e.status == StatusEmprestimo.DEVOLVIDO.value
        assert jogo.status == StatusJogo.DISPONIVEL.value

    def test_cancelar_libera_jogo(self, app, db):
        dono = self._criar_usuario(db, "Dono", "dono@test.com")
        sol = self._criar_usuario(db, "Sol", "sol@test.com")
        jogo = self._criar_jogo(db, "Catan", dono.id)
        prazo = datetime.utcnow() + timedelta(days=7)

        e = Emprestimo()
        e.solicitar(sol, jogo, prazo)
        db.session.add(e)
        db.session.commit()
        e.cancelar()

        assert e.status == StatusEmprestimo.CANCELADO.value
        assert jogo.status == StatusJogo.DISPONIVEL.value

    def test_verificar_atraso_false_dentro_do_prazo(self, app, db):
        dono = self._criar_usuario(db, "Dono", "dono@test.com")
        sol = self._criar_usuario(db, "Sol", "sol@test.com")
        jogo = self._criar_jogo(db, "Catan", dono.id)
        prazo = datetime.utcnow() + timedelta(days=7)

        e = Emprestimo()
        e.solicitar(sol, jogo, prazo)
        db.session.add(e)
        db.session.commit()

        assert e.verificar_atraso() is False

    def test_verificar_atraso_true_prazo_vencido(self, app, db):
        dono = self._criar_usuario(db, "Dono", "dono@test.com")
        sol = self._criar_usuario(db, "Sol", "sol@test.com")
        jogo = self._criar_jogo(db, "Catan", dono.id)
        prazo = datetime.utcnow() - timedelta(days=3)

        e = Emprestimo()
        e.solicitar(sol, jogo, prazo)
        db.session.add(e)
        db.session.commit()

        assert e.verificar_atraso() is True

    def test_calcular_dias_atraso(self, app, db):
        dono = self._criar_usuario(db, "Dono", "dono@test.com")
        sol = self._criar_usuario(db, "Sol", "sol@test.com")
        jogo = self._criar_jogo(db, "Catan", dono.id)
        prazo = datetime.utcnow() - timedelta(days=5)

        e = Emprestimo()
        e.solicitar(sol, jogo, prazo)
        db.session.add(e)
        db.session.commit()

        assert e.calcular_dias_atraso() >= 5

    def test_sem_atraso_retorna_zero_dias(self, app, db):
        dono = self._criar_usuario(db, "Dono", "dono@test.com")
        sol = self._criar_usuario(db, "Sol", "sol@test.com")
        jogo = self._criar_jogo(db, "Catan", dono.id)
        prazo = datetime.utcnow() + timedelta(days=7)

        e = Emprestimo()
        e.solicitar(sol, jogo, prazo)
        db.session.add(e)
        db.session.commit()

        assert e.calcular_dias_atraso() == 0


# ── PENALIDADE ────────────────────────────────────────────────────────────────

class TestPenalidade:

    def _criar_emprestimo_atrasado(self, db, dias_atraso=3):
        dono = Usuario()
        dono.cadastrar("Dono", f"dono{dias_atraso}@test.com", "senha")
        sol = Usuario()
        sol.cadastrar("Sol", f"sol{dias_atraso}@test.com", "senha")
        db.session.add_all([dono, sol])
        db.session.commit()

        jogo = Jogo()
        jogo.cadastrar("Catan", "Desc", "Estratégia")
        jogo.dono_id = dono.id
        db.session.add(jogo)
        db.session.commit()

        e = Emprestimo()
        e.solicitar(sol, jogo, datetime.utcnow() - timedelta(days=dias_atraso))
        db.session.add(e)
        db.session.commit()
        return e, sol

    def test_aplicar_calcula_valor_multa(self, app, db):
        e, sol = self._criar_emprestimo_atrasado(db, dias_atraso=4)
        p = Penalidade()
        p.aplicar(sol, e)
        db.session.add(p)
        db.session.commit()
        assert p.valor_multa == 4 * MULTA_POR_DIA

    def test_aplicar_bloqueia_usuario(self, app, db):
        e, sol = self._criar_emprestimo_atrasado(db, dias_atraso=2)
        p = Penalidade()
        p.aplicar(sol, e)
        db.session.add(p)
        db.session.commit()
        assert sol.status == StatusUsuario.BLOQUEADO.value

    def test_multa_minima_um_dia(self, app, db):
        e, sol = self._criar_emprestimo_atrasado(db, dias_atraso=0)
        p = Penalidade()
        p.aplicar(sol, e)
        assert p.valor_multa == MULTA_POR_DIA

    def test_confirmar_pagamento_muda_status_para_paga(self, app, db):
        e, sol = self._criar_emprestimo_atrasado(db, dias_atraso=2)
        p = Penalidade()
        p.aplicar(sol, e)
        db.session.add(p)
        db.session.commit()
        p.confirmar_pagamento()
        assert p.status == StatusPenalidade.PAGA.value

    def test_confirmar_pagamento_desbloqueia_usuario(self, app, db):
        e, sol = self._criar_emprestimo_atrasado(db, dias_atraso=2)
        p = Penalidade()
        p.aplicar(sol, e)
        db.session.add(p)
        db.session.commit()
        p.confirmar_pagamento()
        assert sol.status == StatusUsuario.ATIVO.value

    def test_penalidade_inicial_esta_pendente(self, app, db):
        e, sol = self._criar_emprestimo_atrasado(db, dias_atraso=2)
        p = Penalidade()
        p.aplicar(sol, e)
        assert p.status == StatusPenalidade.PENDENTE.value


# ── MENSAGEM ──────────────────────────────────────────────────────────────────

class TestMensagem:

    def test_conteudo_vazio_levanta_erro(self, app):
        m = Mensagem()
        u1 = Usuario()
        u1.cadastrar("U1", "u1@test.com", "senha")
        u2 = Usuario()
        u2.cadastrar("U2", "u2@test.com", "senha")

        class FakeEmp:
            id = "fake-id"

        with pytest.raises(ValueError):
            m.enviar(u1, u2, FakeEmp(), "   ")

    def test_mensagem_inicia_nao_lida(self, app):
        m = Mensagem()
        u1 = Usuario()
        u1.cadastrar("U1", "u1@test.com", "senha")
        u1.id = "id1"
        u2 = Usuario()
        u2.cadastrar("U2", "u2@test.com", "senha")
        u2.id = "id2"

        class FakeEmp:
            id = "fake-id"

        m.enviar(u1, u2, FakeEmp(), "Olá!")
        assert m.lida is False

    def test_marcar_como_lida(self, app, db):
        u1 = Usuario()
        u1.cadastrar("U1", "u1b@test.com", "senha")
        u2 = Usuario()
        u2.cadastrar("U2", "u2b@test.com", "senha")
        db.session.add_all([u1, u2])
        db.session.commit()

        jogo = Jogo()
        jogo.cadastrar("Catan", "Desc", "Estratégia")
        jogo.dono_id = u1.id
        db.session.add(jogo)
        db.session.commit()

        e = Emprestimo()
        e.solicitar(u2, jogo, datetime.utcnow() + timedelta(days=7))
        db.session.add(e)
        db.session.commit()

        m = Mensagem()
        m.enviar(u1, u2, e, "Olá!")
        db.session.add(m)
        db.session.commit()
        m.marcar_como_lida()

        assert m.lida is True