# 🎲 Joga Aí – Sistema de Empréstimo de Jogos

> Plataforma web para empréstimo de jogos físicos de tabuleiro e cartas entre usuários.

| | |
|---|---|
| **Disciplina** | DCC603 – Engenharia de Software I |
| **Instituição** | Universidade Federal de Minas Gerais (UFMG) |
| **Professor** | Eduardo Figueiredo |
| **Tema** | 11 – Sistema de Controle de Empréstimo de Jogos |
| **Equipe** | Álvaro Lima Santos, Beatriz Nogueira Alvares, Lucas Dolabella de Castro Lopes, Sarah Menks Sperber, Vanessa Nascimento Silva |
| **Entrega final** | 10/06/2026 |

---

## Índice

1. [Visão Geral](#visão-geral)
2. [Funcionalidades](#funcionalidades)
3. [Tecnologias](#tecnologias)
4. [Pré-requisitos](#pré-requisitos)
5. [Instalação e Execução](#instalação-e-execução)
6. [Testes](#testes)
7. [Estrutura do Projeto](#estrutura-do-projeto)
8. [Arquitetura](#arquitetura)
9. [Classes e Modelos](#classes-e-modelos)
10. [API REST](#api-rest)
11. [Banco de Dados](#banco-de-dados)
12. [Frontend](#frontend)
13. [Fluxos Principais](#fluxos-principais)

---

## Visão Geral

O **Joga Aí** conecta pessoas que querem emprestar e pegar emprestados jogos físicos (tabuleiro, cartas, RPG). Após se cadastrar, o usuário pode registrar seus jogos disponíveis, buscar jogos de outros usuários, negociar prazos via chat interno e gerenciar todo o ciclo do empréstimo — incluindo confirmação de devolução, aplicação automática de penalidades por atraso e desbloqueio da conta após pagamento de multa.

---

## Funcionalidades

### Requisitos Funcionais

| RF | Descrição | Status |
|----|-----------|:------:|
| RF01 | Cadastro de usuários (nome, e-mail, senha criptografada) | ✅ |
| RF02 | Login e logout com autenticação JWT | ✅ |
| RF03 | Cadastrar jogos disponíveis para empréstimo | ✅ |
| RF04 | Visualizar todos os jogos disponíveis na plataforma | ✅ |
| RF05 | Busca de jogos por nome ou categoria | ✅ |
| RF06 | Solicitar empréstimo de um jogo disponível | ✅ |
| RF07 | Definir prazo de devolução no momento da solicitação | ✅ |
| RF08 | Registrar todas as informações do empréstimo | ✅ |
| RF09 | Chat interno vinculado ao empréstimo para negociação | ✅ |
| RF10 | E-mail ao dono no vencimento do prazo de devolução | ✅ stub |
| RF11 | Dono do jogo confirma devolução | ✅ |
| RF12 | Bloquear usuário inadimplente (não devolveu no prazo) | ✅ |
| RF13 | Aplicar multa por atraso (R$ 5,00 por dia) | ✅ |
| RF14 | Desbloquear conta após pagamento da multa | ✅ |
| RF17 | Indicar status do jogo (disponível / emprestado) | ✅ |
| RF18 | Cancelar solicitação de empréstimo antes da devolução | ✅ |
| RF19 | Notificações internas no sistema com badge no navbar | ✅ |

### Requisitos Não Funcionais Atendidos

| RNF | Descrição |
|-----|-----------|
| RNF01 | Interface simples e intuitiva (SPA sem treinamento) |
| RNF05 | Dados protegidos — JWT + bcrypt |
| RNF06 | Senhas armazenadas com hash (Werkzeug/bcrypt) |
| RNF07 | Rotas protegidas exigem token JWT válido |
| RNF08 | Integridade dos dados garantida por transações SQLAlchemy |
| RNF09 | Um jogo não pode estar disponível e emprestado ao mesmo tempo |
| RNF12 | Arquitetura modular em camadas facilita manutenção |
| RNF13 | Acessível em qualquer navegador moderno (desktop e mobile) |

---

## Tecnologias

| Camada | Tecnologia | Versão |
|--------|-----------|--------|
| Backend | Python + Flask | 3.x / 3.0.3 |
| ORM | Flask-SQLAlchemy | 3.1.1 |
| Banco de dados | SQLite | embutido |
| Autenticação | PyJWT | 2.8.0 |
| Segurança de senhas | Werkzeug (bcrypt) | 3.0.3 |
| Testes | pytest | 9.x |
| Frontend | HTML5 + CSS3 + JavaScript | vanilla (sem framework) |

---

## Pré-requisitos

- Python 3.10 ou superior
- pip

Verifique sua versão:
```bash
python3 --version
```

---

## Instalação e Execução

```bash
# 1. Clone o repositório
git clone <url-do-repositorio>
cd TP-Engenharia-de-Software-I

# 2. Crie e ative o ambiente virtual
python3 -m venv venv
source venv/bin/activate        # macOS / Linux
# venv\Scripts\activate         # Windows

# 3. Instale as dependências
pip install -r requirements.txt

# 4. Inicie o servidor
python run.py

# 5. Acesse no navegador
# http://localhost:5000
```

O banco de dados SQLite é criado automaticamente em `instance/jogaai.db` na primeira execução.

Para parar o servidor: `Ctrl + C`

---

## Testes

O projeto possui **66 testes** divididos em duas suites:

### Executar todos os testes

```bash
python -m pytest tests/ -v
```

### Executar apenas testes unitários

```bash
python -m pytest tests/test_unitario.py -v
```

### Executar apenas testes de integração

```bash
python -m pytest tests/test_integracao.py -v
```

### Resultado esperado

```
66 passed in ~9s
```

### Descrição das suites

#### `tests/test_unitario.py` — 35 testes

Testam as classes de negócio isoladamente, sem HTTP nem banco de dados em disco.

| Classe | Testes | O que verifica |
|--------|--------|----------------|
| `TestUsuario` | 10 | Hash de senha, login, bloqueio, desbloqueio, atualização de perfil, `to_dict` sem expor senha |
| `TestJogo` | 6 | Status inicial, validação de campos obrigatórios, disponibilidade, atualização |
| `TestEmprestimo` | 9 | Solicitar, cancelar, confirmar devolução, verificar atraso, calcular dias, validações de bloqueio/disponibilidade/dono |
| `TestPenalidade` | 6 | Cálculo da multa, bloqueio do usuário, multa mínima, pagamento, desbloqueio, status inicial |
| `TestMensagem` | 4 | Conteúdo vazio, mensagem inicia não lida, marcar como lida |

#### `tests/test_integracao.py` — 31 testes

Testam os fluxos completos via API REST usando o Flask test client com banco SQLite em memória. Cobrem os cenários de uso definidos na Sprint 2.

| Classe | Testes | Cenário de uso |
|--------|--------|----------------|
| `TestAutenticacao` | 6 | Cadastro, login, token, rotas protegidas |
| `TestJogos` | 7 | CRUD de jogos, busca, permissões |
| `TestSolicitarEmprestimo` | 5 | Solicitar, indisponibilidade, validações, cancelar |
| `TestConfirmarDevolucao` | 3 | Confirmar devolução, liberar jogo, permissão |
| `TestAplicarPenalidade` | 3 | Bloqueio, usuário bloqueado não solicita, valor da multa |
| `TestPagamentoMulta` | 3 | Pagar multa, desbloquear, permissão de pagamento |
| `TestChat` | 4 | Enviar mensagem, listar, mensagem vazia, acesso de terceiros |

---

## Estrutura do Projeto

```
TP-Engenharia-de-Software-I/
│
├── run.py                          # Ponto de entrada da aplicação
├── requirements.txt                # Dependências Python
│
├── app/
│   ├── __init__.py                 # App factory — create_app()
│   ├── database.py                 # Instância do SQLAlchemy (db)
│   │
│   ├── models/                     # CAMADA DE NEGÓCIO — Classes OOP
│   │   ├── __init__.py
│   │   ├── usuario.py              # Usuario + StatusUsuario enum
│   │   ├── jogo.py                 # Jogo + StatusJogo enum
│   │   ├── emprestimo.py           # Emprestimo + StatusEmprestimo enum
│   │   ├── mensagem.py             # Mensagem (chat interno)
│   │   ├── notificacao.py          # Notificacao + TipoNotificacao enum
│   │   └── penalidade.py           # Penalidade + StatusPenalidade enum
│   │
│   ├── services/                   # CAMADA DE APLICAÇÃO — Lógica de negócio
│   │   ├── auth_service.py         # Registro, login, geração de JWT
│   │   ├── jogo_service.py         # CRUD de jogos, busca
│   │   ├── emprestimo_service.py   # Solicitar, confirmar, cancelar, penalizar
│   │   ├── chat_service.py         # Envio e listagem de mensagens
│   │   └── penalidade_service.py   # Processamento de pagamento de multa
│   │
│   ├── routes/                     # CAMADA DE APRESENTAÇÃO — API REST
│   │   ├── middleware.py           # Decorator requer_autenticacao (JWT)
│   │   ├── auth.py                 # /api/auth/*
│   │   ├── jogos.py                # /api/jogos/*
│   │   ├── emprestimos.py          # /api/emprestimos/*
│   │   ├── chat.py                 # /api/chat/*
│   │   ├── penalidades.py          # /api/penalidades/*
│   │   └── notificacoes.py         # /api/notificacoes/*
│   │
│   └── external/                   # SISTEMAS EXTERNOS (stubs)
│       ├── email_service.py        # Notificações por e-mail
│       └── payment_service.py      # Processamento de pagamentos
│
├── templates/
│   └── index.html                  # SPA principal (único HTML)
│
├── static/
│   ├── css/
│   │   └── style.css               # Estilos globais
│   └── js/
│       ├── api.js                  # Wrapper Fetch API (tokens, headers)
│       ├── auth.js                 # Login e cadastro
│       ├── jogos.js                # Explorar jogos + gerenciar meus jogos
│       ├── emprestimos.js          # Empréstimos, penalidades, notificações
│       ├── chat.js                 # Chat com polling a cada 4s
│       └── app.js                  # Roteador SPA, inicialização
│
├── tests/
│   ├── conftest.py                 # Fixtures pytest (app, client, db em memória)
│   ├── test_unitario.py            # 35 testes unitários das classes OOP
│   └── test_integracao.py          # 31 testes de integração via API REST
│
├── instance/
│   └── jogaai.db                   # Banco SQLite (gerado automaticamente)
│
├── Documentacao_JogaAi_Sprint3.pdf # Documentação técnica completa
├── gerar_pdf.py                    # Script que gera o PDF de documentação
└── Documents/                      # PDFs das sprints anteriores
```

---

## Arquitetura

O sistema adota a **Arquitetura em Camadas (Layered Architecture)** definida na Sprint 2, com cinco camadas bem separadas:

```
┌─────────────────────────────────────────────────┐
│         APRESENTAÇÃO (templates/ + static/)      │
│         SPA: HTML, CSS, JavaScript vanilla        │
└────────────────────┬────────────────────────────┘
                     │ HTTP / JSON
┌────────────────────▼────────────────────────────┐
│         APLICAÇÃO (app/routes/)                   │
│         API REST — 6 blueprints Flask             │
└────────────────────┬────────────────────────────┘
                     │ chamadas de método
┌────────────────────▼────────────────────────────┐
│         NEGÓCIO (app/models/ + app/services/)     │
│         6 classes OOP + 5 serviços                │
└────────────────────┬────────────────────────────┘
                     │ SQLAlchemy ORM
┌────────────────────▼────────────────────────────┐
│         DADOS (SQLite — instance/jogaai.db)       │
└─────────────────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────┐
│         SISTEMAS EXTERNOS (app/external/)         │
│         EmailService + PaymentService (stubs)     │
└─────────────────────────────────────────────────┘
```

---

## Classes e Modelos

As 6 classes foram implementadas diretamente a partir do **Diagrama de Classes da Sprint 2**, mantendo os mesmos atributos, métodos, visibilidades e enumerações.

### `Usuario`
```
status: ATIVO | INATIVO | BLOQUEADO
+ cadastrar(nome, email, senha)
+ login(email, senha) → bool
+ bloquear() / desbloquear()
# _validar_senha(senha) → bool   [privado]
```

### `Jogo`
```
status: DISPONIVEL | EMPRESTADO
+ cadastrar(nome, descricao, categoria)
+ verificar_disponibilidade() → bool
+ atualizar_status(status)
+ buscar(termo) → List[Jogo]       [estático]
# _validar_dados() → bool          [privado]
```

### `Emprestimo`
```
status: ATIVO | DEVOLVIDO | CANCELADO
+ solicitar(solicitante, jogo, data_prazo)
+ confirmar_devolucao()
+ cancelar()
+ verificar_atraso() → bool
+ calcular_dias_atraso() → int
# _validar_solicitacao() → bool    [privado]
```

### `Mensagem`
```
+ enviar(remetente, destinatario, emprestimo, conteudo)
+ marcar_como_lida()
+ listar_por_emprestimo(id) → List  [estático]
# _validar_conteudo() → bool        [privado]
```

### `Notificacao`
```
tipo: SOLICITACAO_EMPRESTIMO | PRAZO_VENCIDO | DEVOLUCAO_CONFIRMADA
    | NOVA_MENSAGEM | PENALIDADE_APLICADA
+ enviar(destinatario, tipo, emprestimo)
+ marcar_como_lida()
# _gerar_mensagem(tipo) → str       [privado]
```

### `Penalidade`
```
status: PENDENTE | PAGA | CANCELADA
valor: R$ 5,00 × dias_de_atraso (mínimo R$ 5,00)
+ aplicar(usuario, emprestimo)      → bloqueia usuário
+ confirmar_pagamento()             → desbloqueia usuário
# _calcular_multa(dias) → float     [privado]
# _bloquear_usuario(usuario)        [privado]
```

---

## API REST

Todas as rotas autenticadas exigem o header:
```
Authorization: Bearer <token_jwt>
```

### Autenticação — `/api/auth`

| Método | Rota | Auth | Descrição |
|--------|------|:----:|-----------|
| POST | `/api/auth/cadastrar` | ❌ | Cria conta, retorna JWT |
| POST | `/api/auth/login` | ❌ | Login, retorna JWT |
| GET | `/api/auth/perfil` | ✅ | Dados do usuário atual |
| PUT | `/api/auth/perfil` | ✅ | Atualiza nome ou senha |

### Jogos — `/api/jogos`

| Método | Rota | Auth | Descrição |
|--------|------|:----:|-----------|
| GET | `/api/jogos` | ❌ | Lista todos os jogos (aceita `?busca=termo`) |
| GET | `/api/jogos/meus` | ✅ | Lista jogos do usuário autenticado |
| GET | `/api/jogos/:id` | ❌ | Detalhe de um jogo |
| POST | `/api/jogos` | ✅ | Cadastra novo jogo |
| PUT | `/api/jogos/:id` | ✅ | Atualiza jogo (somente o dono) |
| DELETE | `/api/jogos/:id` | ✅ | Remove jogo (somente o dono, se disponível) |

### Empréstimos — `/api/emprestimos`

| Método | Rota | Auth | Descrição |
|--------|------|:----:|-----------|
| GET | `/api/emprestimos` | ✅ | Lista empréstimos do usuário (como dono ou solicitante) |
| GET | `/api/emprestimos/:id` | ✅ | Detalhe de um empréstimo |
| POST | `/api/emprestimos` | ✅ | Solicita empréstimo (`jogo_id`, `data_prazo`) |
| PUT | `/api/emprestimos/:id/confirmar-devolucao` | ✅ | Dono confirma que o jogo foi devolvido |
| PUT | `/api/emprestimos/:id/nao-devolvido` | ✅ | Dono reporta não devolução → penalidade aplicada |
| PUT | `/api/emprestimos/:id/cancelar` | ✅ | Cancela empréstimo ativo |

### Chat — `/api/chat`

| Método | Rota | Auth | Descrição |
|--------|------|:----:|-----------|
| GET | `/api/chat/:emprestimo_id` | ✅ | Lista mensagens (marca as não lidas como lidas) |
| POST | `/api/chat/:emprestimo_id` | ✅ | Envia mensagem |

### Penalidades — `/api/penalidades`

| Método | Rota | Auth | Descrição |
|--------|------|:----:|-----------|
| GET | `/api/penalidades` | ✅ | Lista penalidades do usuário |
| POST | `/api/penalidades/:id/pagar` | ✅ | Processa pagamento e desbloqueia a conta |

### Notificações — `/api/notificacoes`

| Método | Rota | Auth | Descrição |
|--------|------|:----:|-----------|
| GET | `/api/notificacoes` | ✅ | Lista notificações do usuário |
| PUT | `/api/notificacoes/:id/lida` | ✅ | Marca uma notificação como lida |
| PUT | `/api/notificacoes/marcar-todas-lidas` | ✅ | Marca todas como lidas |

### Exemplos de requisição

**Cadastrar usuário:**
```bash
curl -X POST http://localhost:5000/api/auth/cadastrar \
  -H "Content-Type: application/json" \
  -d '{"nome": "Lucas", "email": "lucas@email.com", "senha": "minhasenha"}'
```

**Cadastrar jogo (com token):**
```bash
curl -X POST http://localhost:5000/api/jogos \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"nome": "Catan", "descricao": "Jogo de estratégia", "categoria": "Estratégia"}'
```

**Solicitar empréstimo:**
```bash
curl -X POST http://localhost:5000/api/emprestimos \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"jogo_id": "<id>", "data_prazo": "2026-06-20T23:59:59"}'
```

---

## Banco de Dados

Banco SQLite gerado automaticamente em `instance/jogaai.db`.

### Tabelas

| Tabela | Colunas principais |
|--------|--------------------|
| `usuarios` | id, nome, email, senha, status, avaliacao, data_cadastro |
| `jogos` | id, nome, descricao, categoria, status, dono_id, data_cadastro |
| `emprestimos` | id, dono_id, solicitante_id, jogo_id, status, data_inicio, data_prazo, data_devolvido |
| `mensagens` | id, remetente_id, destinatario_id, emprestimo_id, conteudo, lida, data_envio |
| `notificacoes` | id, destinatario_id, mensagem, tipo, lida, data_envio, emprestimo_id |
| `penalidades` | id, usuario_id, emprestimo_id, valor_multa, status, data_aplicacao, data_pagamento |

### Visualizar os dados

```bash
# Instalar DB Browser (macOS)
brew install db-browser-for-sqlite
open -a "DB Browser for SQLite"
# Abrir: instance/jogaai.db

# Ou via terminal
sqlite3 instance/jogaai.db
.tables
SELECT * FROM usuarios;
SELECT * FROM emprestimos;
.quit
```

---

## Frontend

SPA (Single Page Application) em HTML/CSS/JavaScript puro — sem frameworks, sem build step.

### Telas

| Tela | Arquivo JS | Funcionalidades |
|------|-----------|-----------------|
| Login / Cadastro | `auth.js` | Formulários com validação, armazena JWT no localStorage |
| Explorar Jogos | `jogos.js` | Grid de jogos com busca em tempo real (debounce 300ms) |
| Meus Jogos | `jogos.js` | CRUD completo — adicionar, editar, remover jogos |
| Empréstimos | `emprestimos.js` | Lista empréstimos ativos, histórico, ações por papel (dono/solicitante) |
| Chat | `chat.js` | Mensagens com auto-refresh a cada 4 segundos |
| Penalidades | `emprestimos.js` | Visualizar multas pendentes, pagar com um clique |
| Notificações | `emprestimos.js` | Centro de notificações, badge com contador no navbar |

### Autenticação no frontend

O token JWT é salvo no `localStorage` após login/cadastro e enviado automaticamente em todas as requisições autenticadas via `api.js`:

```javascript
headers: { "Authorization": `Bearer ${token}` }
```

---

## Fluxos Principais

### Fluxo de Empréstimo
```
Solicitante                Sistema                     Dono
     │                        │                          │
     │── busca jogo ──────────▶│                          │
     │◀─ lista jogos ──────────│                          │
     │── solicita empréstimo ──▶│                          │
     │                        │── jogo = EMPRESTADO       │
     │                        │── notifica dono ──────────▶│
     │◀────────────────────────│                          │
     │◀──────── chat ──────────────────────────────────────│
     │                        │                          │
     │                        │◀── confirma devolução ────│
     │                        │── jogo = DISPONIVEL       │
     │◀── notificação ─────────│                          │
```

### Fluxo de Penalidade
```
         Dono reporta não devolução
                    │
         Sistema calcula dias × R$5,00
                    │
         Penalidade PENDENTE criada
                    │
         Solicitante BLOQUEADO
                    │
         Solicitante acessa "Penalidades"
                    │
         Clica em "Pagar Multa"
                    │
         PaymentService.processar() → aprovado
                    │
         Penalidade PAGA + Usuário ATIVO
```

---

## Sistemas Externos (Stubs)

Em produção, substituir os stubs por integrações reais sem alterar nenhuma outra camada:

| Serviço | Stub atual | Integração sugerida |
|---------|-----------|---------------------|
| E-mail | Log no console | SendGrid / SMTP |
| Pagamento | Sempre aprova | Stripe / MercadoPago |