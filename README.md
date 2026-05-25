# Joga Aí – Sistema de Empréstimo de Jogos

**Disciplina:** DCC603 – Engenharia de Software I | UFMG  
**Tema 11:** Sistema de Controle de Empréstimo de Jogos  
**Equipe:** Álvaro Lima, Beatriz Nogueira, Lucas Dolabella, Sarah Menks, Vanessa Nascimento

---

## Como executar

```bash
# 1. Instalar dependências
pip install -r requirements.txt

# 2. Iniciar o servidor
python run.py

# 3. Abrir no navegador: http://localhost:5000
```

---

## Arquitetura (Layered Architecture)

```
app/
├── models/           # Camada de Negócio – classes OOP (mapeia o Diagrama de Classes)
│   ├── usuario.py    # Usuario, StatusUsuario (ATIVO/INATIVO/BLOQUEADO)
│   ├── jogo.py       # Jogo, StatusJogo (DISPONIVEL/EMPRESTADO)
│   ├── emprestimo.py # Emprestimo, StatusEmprestimo (ATIVO/DEVOLVIDO/CANCELADO)
│   ├── mensagem.py   # Mensagem (chat interno)
│   ├── notificacao.py# Notificacao, TipoNotificacao
│   └── penalidade.py # Penalidade, StatusPenalidade (PENDENTE/PAGA/CANCELADA)
├── services/         # Camada de Aplicação – orquestra regras de negócio
├── routes/           # Camada de Apresentação – API REST
├── external/         # Sistemas Externos (e-mail e pagamento, stubs)
└── database.py       # Camada de Dados – SQLAlchemy + SQLite

static/               # Frontend SPA
templates/index.html
```

## Tecnologias

- **Backend:** Python 3 + Flask + SQLAlchemy + PyJWT
- **Banco de dados:** SQLite (`instance/jogaai.db`)
- **Frontend:** HTML5 + CSS3 + JavaScript vanilla (SPA)

## Funcionalidades

| RF | Descrição | Status |
|----|-----------|--------|
| RF01 | Cadastro de usuários | ✅ |
| RF02 | Login / Logout (JWT) | ✅ |
| RF03 | Cadastrar jogos | ✅ |
| RF04 | Visualizar jogos disponíveis | ✅ |
| RF05 | Busca por nome/categoria | ✅ |
| RF06 | Solicitar empréstimo | ✅ |
| RF07 | Definir prazo de devolução | ✅ |
| RF08 | Registrar empréstimo | ✅ |
| RF09 | Chat interno vinculado ao empréstimo | ✅ |
| RF10 | E-mail ao dono no vencimento do prazo | ✅ (stub) |
| RF11 | Confirmar devolução | ✅ |
| RF12 | Bloquear usuário inadimplente | ✅ |
| RF13 | Aplicar multa (R$5/dia de atraso) | ✅ |
| RF14 | Desbloquear após pagamento de multa | ✅ |
| RF17 | Status do jogo (disponível/emprestado) | ✅ |
| RF18 | Cancelar solicitação de empréstimo | ✅ |
| RF19 | Notificações internas no sistema | ✅ |