from fpdf import FPDF

FONT_R = "/System/Library/Fonts/Supplemental/Arial.ttf"
FONT_B = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"
FONT_I = "/System/Library/Fonts/Supplemental/Arial Italic.ttf"
FONT_MONO = "/System/Library/Fonts/Supplemental/Courier New.ttf"

class PDF(FPDF):
    def __init__(self):
        super().__init__()
        self.add_font("Arial", "", FONT_R)
        self.add_font("Arial", "B", FONT_B)
        self.add_font("Arial", "I", FONT_I)
        self.add_font("Mono", "", FONT_MONO)

    def header(self):
        self.set_font("Arial", "B", 10)
        self.set_text_color(108, 71, 255)
        self.cell(0, 8, "Joga Aí - Sistema de Emprestimo de Jogos | DCC603 UFMG", align="C")
        self.ln(4)
        self.set_draw_color(108, 71, 255)
        self.set_line_width(0.5)
        self.line(10, self.get_y(), 200, self.get_y())
        self.ln(4)

    def footer(self):
        self.set_y(-12)
        self.set_font("Arial", "I", 8)
        self.set_text_color(150, 150, 150)
        self.cell(0, 8, f"Página {self.page_no()}", align="C")

    def titulo(self, texto):
        self.ln(4)
        self.set_font("Arial", "B", 14)
        self.set_text_color(108, 71, 255)
        self.cell(0, 8, texto)
        self.ln(2)
        self.set_draw_color(200, 190, 255)
        self.set_line_width(0.3)
        self.line(10, self.get_y(), 200, self.get_y())
        self.ln(5)
        self.set_text_color(30, 30, 30)

    def subtitulo(self, texto):
        self.ln(2)
        self.set_font("Arial", "B", 11)
        self.set_text_color(50, 50, 50)
        self.cell(0, 7, texto)
        self.ln(5)
        self.set_text_color(30, 30, 30)

    def corpo(self, texto):
        self.set_font("Arial", "", 10)
        self.set_text_color(40, 40, 40)
        self.multi_cell(0, 5.5, texto)
        self.ln(2)

    def codigo(self, texto):
        self.set_font("Mono", "", 9)
        self.set_fill_color(245, 245, 250)
        self.set_text_color(30, 30, 80)
        self.multi_cell(0, 5, texto, fill=True)
        self.set_font("Arial", "", 10)
        self.set_text_color(40, 40, 40)
        self.ln(2)

    def bullet(self, texto):
        self.set_font("Arial", "", 10)
        self.set_text_color(40, 40, 40)
        self.cell(6, 5.5, "•")
        self.multi_cell(0, 5.5, texto)

    def tabela(self, cabecalhos, linhas, larguras):
        self.set_font("Arial", "B", 9)
        self.set_fill_color(108, 71, 255)
        self.set_text_color(255, 255, 255)
        for i, h in enumerate(cabecalhos):
            self.cell(larguras[i], 7, h, border=1, fill=True)
        self.ln()
        self.set_font("Arial", "", 9)
        fill = False
        for linha in linhas:
            self.set_fill_color(240, 237, 255) if fill else self.set_fill_color(255, 255, 255)
            self.set_text_color(30, 30, 30)
            for i, cel in enumerate(linha):
                self.cell(larguras[i], 6, str(cel), border=1, fill=True)
            self.ln()
            fill = not fill
        self.ln(3)


pdf = PDF()
pdf.set_auto_page_break(auto=True, margin=15)
pdf.add_page()

# ── CAPA ──────────────────────────────────────────────────────────────────────
pdf.ln(20)
pdf.set_font("Arial", "B", 28)
pdf.set_text_color(108, 71, 255)
pdf.cell(0, 14, "Joga Aí", align="C")
pdf.ln(10)
pdf.set_font("Arial", "B", 16)
pdf.set_text_color(60, 60, 60)
pdf.cell(0, 10, "Sistema de Empréstimo de Jogos de Tabuleiro", align="C")
pdf.ln(8)
pdf.set_font("Arial", "", 11)
pdf.set_text_color(100, 100, 100)
pdf.cell(0, 7, "Sprint 3 – Documentação Técnica de Implementação", align="C")
pdf.ln(16)
pdf.set_draw_color(200, 190, 255)
pdf.set_line_width(0.5)
pdf.line(40, pdf.get_y(), 170, pdf.get_y())
pdf.ln(10)
pdf.set_font("Arial", "", 10)
pdf.set_text_color(80, 80, 80)
dados_capa = [
    ("Disciplina", "DCC603 – Engenharia de Software I"),
    ("Instituição", "Universidade Federal de Minas Gerais (UFMG)"),
    ("Professor", "Eduardo Figueiredo"),
    ("Tema", "11 – Sistema de Controle de Empréstimo de Jogos"),
    ("Equipe", "Álvaro Lima, Beatriz Nogueira, Lucas Dolabella,"),
    ("", "Sarah Menks, Vanessa Nascimento"),
]
for chave, valor in dados_capa:
    if chave:
        pdf.set_font("Arial", "B", 10)
        pdf.cell(35, 7, chave + ":")
    else:
        pdf.cell(35, 7, "")
    pdf.set_font("Arial", "", 10)
    pdf.cell(0, 7, valor)
    pdf.ln()

# ── 1. VISÃO GERAL ────────────────────────────────────────────────────────────
pdf.add_page()
pdf.titulo("1. Visão Geral do Sistema")
pdf.corpo(
    "O Joga Aí é uma plataforma web que conecta pessoas interessadas em emprestar e pegar "
    "emprestados jogos físicos, como jogos de tabuleiro e cartas. O sistema foi desenvolvido "
    "como trabalho prático da disciplina DCC603 – Engenharia de Software I, seguindo o "
    "processo ágil SCRUM com desenvolvimento incremental ao longo de 3 sprints."
)
pdf.corpo(
    "O objetivo central é permitir que usuários cadastrem seus jogos disponíveis, pesquisem "
    "jogos de outros usuários, negociem prazos via chat interno e gerenciem o ciclo completo "
    "de empréstimo, incluindo controle de prazos, notificações, penalidades por atraso e "
    "desbloqueio mediante pagamento de multa."
)

pdf.subtitulo("1.1 Tecnologias Utilizadas")
pdf.tabela(
    ["Componente", "Tecnologia", "Justificativa"],
    [
        ["Backend", "Python 3 + Flask", "OOP nativo, estrutura modular clara, REST simples"],
        ["ORM / Dados", "SQLAlchemy + SQLite", "Sem setup, arquivo único, ORM robusto"],
        ["Autenticação", "JWT (PyJWT)", "Stateless, ideal para APIs REST"],
        ["Senhas", "Werkzeug (bcrypt)", "Hash seguro incluído no Flask"],
        ["Frontend", "HTML5 + CSS3 + JS", "SPA vanilla, sem build step, zero dependências"],
    ],
    [40, 50, 100]
)

pdf.subtitulo("1.2 Como Executar")
pdf.codigo(
    "# 1. Criar e ativar ambiente virtual\n"
    "python3 -m venv venv\n"
    "source venv/bin/activate\n\n"
    "# 2. Instalar dependências\n"
    "pip install -r requirements.txt\n\n"
    "# 3. Iniciar o servidor\n"
    "python run.py\n\n"
    "# 4. Abrir no navegador\n"
    "http://localhost:5000"
)

# ── 2. ARQUITETURA ────────────────────────────────────────────────────────────
pdf.titulo("2. Arquitetura do Sistema")
pdf.corpo(
    "O sistema adota a Arquitetura em Camadas (Layered Architecture), definida na Sprint 2, "
    "organizada em cinco camadas com responsabilidades bem separadas."
)

pdf.subtitulo("2.1 Camadas e Correspondência com o Código")
pdf.tabela(
    ["Camada", "Diretório", "Responsabilidade"],
    [
        ["Apresentação", "templates/ + static/", "Frontend SPA: HTML, CSS, JavaScript"],
        ["Aplicação", "app/routes/", "API REST – recebe requisições, valida, repassa"],
        ["Negócio", "app/models/ + app/services/", "Classes OOP + regras de negócio"],
        ["Dados", "app/database.py + SQLite", "Persistência via SQLAlchemy ORM"],
        ["Sistemas Externos", "app/external/", "E-mail e pagamento (stubs integráveis)"],
    ],
    [38, 52, 100]
)

pdf.subtitulo("2.2 Estrutura de Diretórios")
pdf.codigo(
    "TP-Engenharia-de-Software-I/\n"
    "├── run.py                    # Ponto de entrada\n"
    "├── requirements.txt          # Flask, SQLAlchemy, PyJWT, Werkzeug\n"
    "├── app/\n"
    "│   ├── __init__.py           # App factory (create_app)\n"
    "│   ├── database.py           # Instância do SQLAlchemy\n"
    "│   ├── models/               # Camada de Negócio – Classes OOP\n"
    "│   │   ├── usuario.py        # Classe Usuario + StatusUsuario\n"
    "│   │   ├── jogo.py           # Classe Jogo + StatusJogo\n"
    "│   │   ├── emprestimo.py     # Classe Emprestimo + StatusEmprestimo\n"
    "│   │   ├── mensagem.py       # Classe Mensagem (chat)\n"
    "│   │   ├── notificacao.py    # Classe Notificacao + TipoNotificacao\n"
    "│   │   └── penalidade.py     # Classe Penalidade + StatusPenalidade\n"
    "│   ├── services/             # Camada de Aplicação – Serviços\n"
    "│   │   ├── auth_service.py\n"
    "│   │   ├── jogo_service.py\n"
    "│   │   ├── emprestimo_service.py\n"
    "│   │   ├── chat_service.py\n"
    "│   │   └── penalidade_service.py\n"
    "│   ├── routes/               # Camada de Apresentação – API REST\n"
    "│   │   ├── auth.py\n"
    "│   │   ├── jogos.py\n"
    "│   │   ├── emprestimos.py\n"
    "│   │   ├── chat.py\n"
    "│   │   ├── penalidades.py\n"
    "│   │   └── notificacoes.py\n"
    "│   └── external/             # Sistemas Externos\n"
    "│       ├── email_service.py\n"
    "│       └── payment_service.py\n"
    "├── templates/index.html      # SPA principal\n"
    "├── static/css/style.css\n"
    "└── static/js/                # api.js, auth.js, jogos.js, emprestimos.js,\n"
    "                              # chat.js, app.js"
)

# ── 3. DIAGRAMA DE CLASSES ────────────────────────────────────────────────────
pdf.add_page()
pdf.titulo("3. Classes OOP – Implementação do Diagrama de Classes")
pdf.corpo(
    "As seis classes principais do sistema foram implementadas diretamente a partir do "
    "Diagrama de Classes definido na Sprint 2, mantendo os mesmos atributos, métodos, "
    "visibilidades e enumerações. Cada classe estende db.Model (SQLAlchemy), unindo "
    "persistência e comportamento em um único objeto orientado a objetos."
)

pdf.subtitulo("3.1 Usuario (app/models/usuario.py)")
pdf.tabela(
    ["Atributo / Método", "Tipo", "Descrição"],
    [
        ["id", "String (UUID)", "Identificador único gerado automaticamente"],
        ["nome", "String", "Nome completo do usuário"],
        ["email", "String (único)", "E-mail usado no login"],
        ["senha", "String", "Hash bcrypt da senha"],
        ["status", "StatusUsuario", "ATIVO / INATIVO / BLOQUEADO"],
        ["avaliacao", "Float", "Média de avaliações recebidas"],
        ["data_cadastro", "DateTime", "Data de criação da conta"],
        ["cadastrar()", "void", "Inicializa e salva o usuário com senha hasheada"],
        ["login()", "bool", "Valida e-mail e senha"],
        ["bloquear()", "void", "Muda status para BLOQUEADO"],
        ["desbloquear()", "void", "Muda status para ATIVO"],
        ["_validar_senha()", "bool", "Método privado: verifica hash da senha"],
    ],
    [60, 35, 95]
)

pdf.subtitulo("3.2 Jogo (app/models/jogo.py)")
pdf.tabela(
    ["Atributo / Método", "Tipo", "Descrição"],
    [
        ["id", "String (UUID)", "Identificador único"],
        ["nome", "String", "Nome do jogo"],
        ["descricao", "Text", "Descrição completa"],
        ["categoria", "String", "Ex: Estratégia, Cartas, RPG"],
        ["status", "StatusJogo", "DISPONIVEL / EMPRESTADO"],
        ["dono_id", "FK -> Usuario", "Usuário dono do jogo"],
        ["cadastrar()", "void", "Valida e inicializa o jogo"],
        ["verificar_disponibilidade()", "bool", "Retorna true se status = DISPONIVEL"],
        ["atualizar_status()", "void", "Muda o status do jogo"],
        ["buscar(termo)", "List<Jogo>", "Busca por nome ou categoria (ILIKE)"],
        ["_validar_dados()", "bool", "Método privado: valida campos obrigatórios"],
    ],
    [60, 35, 95]
)

pdf.subtitulo("3.3 Emprestimo (app/models/emprestimo.py)")
pdf.tabela(
    ["Atributo / Método", "Tipo", "Descrição"],
    [
        ["id", "String (UUID)", "Identificador único"],
        ["dono_id", "FK -> Usuario", "Dono do jogo"],
        ["solicitante_id", "FK -> Usuario", "Quem pegou emprestado"],
        ["jogo_id", "FK -> Jogo", "Jogo emprestado"],
        ["status", "StatusEmprestimo", "ATIVO / DEVOLVIDO / CANCELADO"],
        ["data_inicio", "DateTime", "Data da solicitação"],
        ["data_prazo", "DateTime", "Prazo acordado para devolução"],
        ["data_devolvido", "DateTime", "Data real de devolução (nullable)"],
        ["solicitar()", "void", "Valida e registra o empréstimo"],
        ["confirmar_devolucao()", "void", "Marca devolvido e libera o jogo"],
        ["cancelar()", "void", "Cancela e libera o jogo"],
        ["verificar_atraso()", "bool", "True se data atual > data_prazo e ATIVO"],
        ["calcular_dias_atraso()", "int", "Dias entre prazo e hoje"],
        ["_validar_solicitacao()", "bool", "Privado: verifica bloqueio, disponibilidade"],
    ],
    [60, 35, 95]
)

pdf.add_page()
pdf.subtitulo("3.4 Mensagem (app/models/mensagem.py)")
pdf.tabela(
    ["Atributo / Método", "Tipo", "Descrição"],
    [
        ["id", "String (UUID)", "Identificador único"],
        ["remetente_id", "FK -> Usuario", "Quem enviou a mensagem"],
        ["destinatario_id", "FK -> Usuario", "Quem recebe"],
        ["emprestimo_id", "FK -> Emprestimo", "Chat vinculado ao empréstimo"],
        ["conteudo", "Text", "Texto da mensagem"],
        ["lida", "Boolean", "Se o destinatário já leu"],
        ["data_envio", "DateTime", "Momento do envio"],
        ["enviar()", "void", "Valida e prepara a mensagem"],
        ["marcar_como_lida()", "void", "Marca lida = True"],
        ["listar_por_emprestimo()", "List", "Retorna histórico ordenado por data"],
        ["_validar_conteudo()", "bool", "Privado: impede mensagem vazia"],
    ],
    [60, 35, 95]
)

pdf.subtitulo("3.5 Notificacao (app/models/notificacao.py)")
pdf.tabela(
    ["Atributo / Método", "Tipo", "Descrição"],
    [
        ["id", "String (UUID)", "Identificador único"],
        ["destinatario_id", "FK -> Usuario", "Quem recebe a notificação"],
        ["mensagem", "Text", "Texto gerado automaticamente"],
        ["tipo", "TipoNotificacao", "SOLICITACAO_EMPRESTIMO, PRAZO_VENCIDO,"],
        ["", "", "DEVOLUCAO_CONFIRMADA, NOVA_MENSAGEM, PENALIDADE_APLICADA"],
        ["lida", "Boolean", "Se o usuário já viu"],
        ["data_envio", "DateTime", "Momento do envio"],
        ["emprestimo_id", "FK -> Emprestimo", "Empréstimo relacionado (opcional)"],
        ["enviar()", "void", "Inicializa e gera a mensagem pelo tipo"],
        ["marcar_como_lida()", "void", "Marca lida = True"],
        ["_gerar_mensagem()", "str", "Privado: texto descritivo por tipo"],
    ],
    [60, 35, 95]
)

pdf.subtitulo("3.6 Penalidade (app/models/penalidade.py)")
pdf.tabela(
    ["Atributo / Método", "Tipo", "Descrição"],
    [
        ["id", "String (UUID)", "Identificador único"],
        ["usuario_id", "FK -> Usuario", "Quem recebeu a penalidade"],
        ["emprestimo_id", "FK -> Emprestimo", "Empréstimo em atraso"],
        ["valor_multa", "Float", "R$ 5,00 por dia de atraso"],
        ["status", "StatusPenalidade", "PENDENTE / PAGA / CANCELADA"],
        ["data_aplicacao", "DateTime", "Quando a penalidade foi gerada"],
        ["data_pagamento", "DateTime", "Quando foi quitada (nullable)"],
        ["aplicar()", "void", "Calcula multa e bloqueia o usuário"],
        ["confirmar_pagamento()", "void", "Marca PAGA e desbloqueia o usuário"],
        ["desbloquear_usuario()", "void", "Chama usuario.desbloquear()"],
        ["_calcular_multa()", "float", "Privado: dias_atraso × R$5,00 (mínimo R$5)"],
        ["_bloquear_usuario()", "void", "Privado: chama usuario.bloquear()"],
    ],
    [60, 35, 95]
)

# ── 4. API REST ───────────────────────────────────────────────────────────────
pdf.add_page()
pdf.titulo("4. API REST – Endpoints")

pdf.subtitulo("4.1 Autenticação (/api/auth)")
pdf.tabela(
    ["Método", "Endpoint", "Auth?", "Descrição"],
    [
        ["POST", "/api/auth/cadastrar", "Não", "Registra novo usuário, retorna JWT"],
        ["POST", "/api/auth/login", "Não", "Login com e-mail e senha, retorna JWT"],
        ["GET", "/api/auth/perfil", "Sim", "Retorna dados do usuário autenticado"],
        ["PUT", "/api/auth/perfil", "Sim", "Atualiza nome ou senha"],
    ],
    [18, 60, 16, 96]
)

pdf.subtitulo("4.2 Jogos (/api/jogos)")
pdf.tabela(
    ["Método", "Endpoint", "Auth?", "Descrição"],
    [
        ["GET", "/api/jogos?busca=termo", "Não", "Lista todos os jogos (com busca opcional)"],
        ["GET", "/api/jogos/meus", "Sim", "Lista jogos do usuário autenticado"],
        ["GET", "/api/jogos/:id", "Não", "Detalhe de um jogo"],
        ["POST", "/api/jogos", "Sim", "Cadastra novo jogo"],
        ["PUT", "/api/jogos/:id", "Sim", "Atualiza jogo (somente dono)"],
        ["DELETE", "/api/jogos/:id", "Sim", "Remove jogo (somente dono, se disponível)"],
    ],
    [18, 60, 16, 96]
)

pdf.subtitulo("4.3 Empréstimos (/api/emprestimos)")
pdf.tabela(
    ["Método", "Endpoint", "Auth?", "Descrição"],
    [
        ["GET", "/api/emprestimos", "Sim", "Lista empréstimos do usuário (dono ou solicitante)"],
        ["GET", "/api/emprestimos/:id", "Sim", "Detalhe de um empréstimo"],
        ["POST", "/api/emprestimos", "Sim", "Solicita empréstimo de um jogo"],
        ["PUT", "/api/emprestimos/:id/confirmar-devolucao", "Sim", "Dono confirma devolução"],
        ["PUT", "/api/emprestimos/:id/nao-devolvido", "Sim", "Dono reporta não devolução"],
        ["PUT", "/api/emprestimos/:id/cancelar", "Sim", "Cancela empréstimo ativo"],
    ],
    [18, 75, 16, 81]
)

pdf.subtitulo("4.4 Chat, Penalidades e Notificações")
pdf.tabela(
    ["Método", "Endpoint", "Auth?", "Descrição"],
    [
        ["GET", "/api/chat/:emprestimo_id", "Sim", "Lista mensagens do chat (marca como lidas)"],
        ["POST", "/api/chat/:emprestimo_id", "Sim", "Envia mensagem no chat"],
        ["GET", "/api/penalidades", "Sim", "Lista penalidades do usuário"],
        ["POST", "/api/penalidades/:id/pagar", "Sim", "Processa pagamento e desbloqueia"],
        ["GET", "/api/notificacoes", "Sim", "Lista notificações do usuário"],
        ["PUT", "/api/notificacoes/:id/lida", "Sim", "Marca notificação como lida"],
        ["PUT", "/api/notificacoes/marcar-todas-lidas", "Sim", "Marca todas como lidas"],
    ],
    [18, 75, 16, 81]
)

# ── 5. FLUXOS ─────────────────────────────────────────────────────────────────
pdf.add_page()
pdf.titulo("5. Fluxos Implementados")

pdf.subtitulo("5.1 Fluxo de Empréstimo")
linhas_fluxo = [
    ("1", "Solicitante", "Acessa 'Explorar', encontra jogo disponível"),
    ("2", "Solicitante", "Clica em 'Pegar Emprestado', define prazo de devolução"),
    ("3", "Sistema", "Valida: usuário não bloqueado, jogo disponível, não é o próprio dono"),
    ("4", "Sistema", "Cria Emprestimo (ATIVO), muda status do Jogo para EMPRESTADO"),
    ("5", "Sistema", "Cria Notificacao para o dono (SOLICITACAO_EMPRESTIMO)"),
    ("6", "Ambos", "Podem trocar mensagens via Chat (atualização a cada 4s)"),
    ("7", "Sistema", "No vencimento: envia e-mail ao dono (stub EmailService)"),
    ("8", "Dono", "Confirma devolução → Emprestimo DEVOLVIDO, Jogo DISPONIVEL"),
    ("8b", "Dono", "Ou reporta não devolução → Penalidade aplicada, solicitante BLOQUEADO"),
]
pdf.tabela(["Passo", "Ator", "Ação"], linhas_fluxo, [16, 35, 139])

pdf.subtitulo("5.2 Fluxo de Penalidade e Pagamento")
linhas_pen = [
    ("1", "Sistema", "Dono clica em 'Não Devolvido'"),
    ("2", "Sistema", "Calcula dias de atraso × R$5,00 (mínimo R$5,00)"),
    ("3", "Sistema", "Cria Penalidade (PENDENTE), bloqueia solicitante"),
    ("4", "Sistema", "Cria Notificacao PENALIDADE_APLICADA, envia e-mail"),
    ("5", "Solicitante", "Acessa 'Penalidades', vê valor e motivo"),
    ("6", "Solicitante", "Clica em 'Pagar Multa'"),
    ("7", "Sistema", "PaymentService.processar() → aprovado"),
    ("8", "Sistema", "Penalidade.confirmar_pagamento() → status PAGA"),
    ("9", "Sistema", "usuario.desbloquear() → status ATIVO"),
    ("10", "Sistema", "Envia comprovante por e-mail (stub)"),
]
pdf.tabela(["Passo", "Ator", "Ação"], linhas_pen, [16, 35, 139])

# ── 6. REQUISITOS ─────────────────────────────────────────────────────────────
pdf.add_page()
pdf.titulo("6. Requisitos Implementados")

pdf.subtitulo("6.1 Requisitos Funcionais")
pdf.tabela(
    ["RF", "Descrição", "Status"],
    [
        ["RF01", "Cadastro de usuários (nome, e-mail, senha)", "Implementado"],
        ["RF02", "Login / Logout com autenticação JWT", "Implementado"],
        ["RF03", "Cadastrar jogos disponíveis para empréstimo", "Implementado"],
        ["RF04", "Visualizar jogos disponíveis na plataforma", "Implementado"],
        ["RF05", "Busca de jogos por nome ou categoria", "Implementado"],
        ["RF06", "Solicitar empréstimo de um jogo disponível", "Implementado"],
        ["RF07", "Definir prazo para devolução", "Implementado"],
        ["RF08", "Registrar todas as informações do empréstimo", "Implementado"],
        ["RF09", "Chat interno vinculado ao empréstimo", "Implementado"],
        ["RF10", "E-mail ao dono no vencimento do prazo", "Stub (EmailService)"],
        ["RF11", "Dono confirma devolução do jogo", "Implementado"],
        ["RF12", "Bloquear usuário inadimplente", "Implementado"],
        ["RF13", "Aplicar multa por atraso (R$5/dia)", "Implementado"],
        ["RF14", "Desbloquear após pagamento de multa", "Implementado"],
        ["RF17", "Status do jogo (disponível / emprestado)", "Implementado"],
        ["RF18", "Cancelar solicitação de empréstimo", "Implementado"],
        ["RF19", "Notificações internas no sistema", "Implementado"],
    ],
    [15, 140, 35]
)

pdf.subtitulo("6.2 Requisitos Não Funcionais Atendidos")
pdf.tabela(
    ["RNF", "Descrição", "Como foi atendido"],
    [
        ["RNF01", "Facilidade de uso", "Interface SPA intuitiva, sem treinamento"],
        ["RNF05", "Proteção de dados", "JWT + bcrypt para senhas"],
        ["RNF06", "Criptografia de senha", "Werkzeug generate_password_hash"],
        ["RNF07", "Autenticação restrita", "Middleware requer_autenticacao em todas as rotas"],
        ["RNF08", "Integridade dos dados", "Transações SQLAlchemy + FK constraints"],
        ["RNF09", "Consistência de estados", "Um jogo não pode ser DISPONIVEL e EMPRESTADO"],
        ["RNF12", "Manutenibilidade", "Arquitetura em camadas, módulos independentes"],
        ["RNF13", "Acesso multiplataforma", "Aplicação web acessível em qualquer browser"],
    ],
    [15, 55, 120]
)

# ── 7. SISTEMAS EXTERNOS ──────────────────────────────────────────────────────
pdf.titulo("7. Sistemas Externos (Stubs)")
pdf.corpo(
    "Os sistemas externos foram implementados como stubs (simulações) que registram as "
    "operações no log da aplicação. Em ambiente de produção, esses stubs seriam substituídos "
    "por integrações reais sem alterar nenhuma outra camada do sistema."
)

pdf.subtitulo("7.1 EmailService (app/external/email_service.py)")
pdf.tabela(
    ["Método", "Quando é chamado", "Em produção"],
    [
        ["enviar_aviso_prazo_vencido()", "Prazo do empréstimo vence", "SMTP / SendGrid"],
        ["enviar_confirmacao_devolucao()", "Dono confirma devolução", "SMTP / SendGrid"],
        ["enviar_aviso_penalidade()", "Penalidade aplicada", "SMTP / SendGrid"],
        ["enviar_comprovante_pagamento()", "Multa paga", "SMTP / SendGrid"],
    ],
    [65, 65, 60]
)

pdf.subtitulo("7.2 PaymentService (app/external/payment_service.py)")
pdf.tabela(
    ["Método", "Comportamento atual", "Em produção"],
    [
        ["processar(valor, metodo)", "Sempre retorna 'aprovado'", "Stripe / PagSeguro / MercadoPago"],
    ],
    [65, 65, 60]
)

# ── 8. BANCO DE DADOS ─────────────────────────────────────────────────────────
pdf.add_page()
pdf.titulo("8. Banco de Dados")
pdf.corpo(
    "O banco de dados utilizado é o SQLite, armazenado automaticamente no arquivo "
    "instance/jogaai.db ao iniciar a aplicação. O schema é criado pelo SQLAlchemy com "
    "db.create_all() na inicialização."
)

pdf.subtitulo("8.1 Tabelas")
pdf.tabela(
    ["Tabela", "Colunas principais", "Relacionamentos"],
    [
        ["usuarios", "id, nome, email, senha, status, avaliacao", "1:N com jogos, emprestimos, penalidades"],
        ["jogos", "id, nome, descricao, categoria, status, dono_id", "N:1 usuarios, 1:N emprestimos"],
        ["emprestimos", "id, dono_id, solicitante_id, jogo_id, status, datas", "N:1 usuarios/jogos, 1:N mensagens"],
        ["mensagens", "id, remetente_id, destinatario_id, emprestimo_id, conteudo", "N:1 usuarios/emprestimos"],
        ["notificacoes", "id, destinatario_id, mensagem, tipo, lida, emprestimo_id", "N:1 usuarios/emprestimos"],
        ["penalidades", "id, usuario_id, emprestimo_id, valor_multa, status", "N:1 usuarios/emprestimos"],
    ],
    [28, 80, 82]
)

pdf.subtitulo("8.2 Como visualizar os dados")
pdf.corpo("Instale o DB Browser for SQLite e abra o arquivo instance/jogaai.db:")
pdf.codigo(
    "# Instalar via Homebrew (macOS)\n"
    "brew install db-browser-for-sqlite\n\n"
    "# Abrir\n"
    "open -a 'DB Browser for SQLite'\n"
    "# Arquivo: TP-Engenharia-de-Software-I/instance/jogaai.db\n\n"
    "# Ou via terminal\n"
    "sqlite3 instance/jogaai.db\n"
    ".tables\n"
    "SELECT * FROM usuarios;\n"
    "SELECT * FROM emprestimos;"
)

# ── 9. FRONTEND ───────────────────────────────────────────────────────────────
pdf.titulo("9. Frontend – SPA (Single Page Application)")
pdf.corpo(
    "O frontend é uma SPA (Single Page Application) construída com HTML, CSS e JavaScript "
    "puro (vanilla), sem frameworks externos. Todas as telas são renderizadas dinamicamente "
    "por JavaScript no mesmo arquivo index.html."
)

pdf.subtitulo("9.1 Telas Implementadas")
pdf.tabela(
    ["Tela", "Arquivo JS", "Funcionalidades"],
    [
        ["Login / Cadastro", "auth.js", "Formulários de login e registro com JWT"],
        ["Explorar Jogos", "jogos.js (Jogos)", "Grid de jogos, busca em tempo real, solicitar empréstimo"],
        ["Meus Jogos", "jogos.js (MeusJogos)", "CRUD de jogos do usuário autenticado"],
        ["Empréstimos", "emprestimos.js", "Lista empréstimos, confirmar/cancelar/reportar"],
        ["Chat", "chat.js", "Mensagens em tempo real (polling 4s)"],
        ["Penalidades", "emprestimos.js", "Listar e pagar multas pendentes"],
        ["Notificações", "emprestimos.js", "Centro de notificações com badge no navbar"],
    ],
    [38, 42, 110]
)

pdf.subtitulo("9.2 Comunicação com o Backend")
pdf.corpo(
    "Todas as chamadas ao backend são feitas via Fetch API (JavaScript nativo) através do "
    "objeto Api definido em static/js/api.js. O token JWT é armazenado no localStorage e "
    "enviado automaticamente no header Authorization: Bearer <token> em todas as requisições "
    "autenticadas."
)

pdf.output("Documentacao_JogaAi_Sprint3.pdf")
print("PDF gerado: Documentacao_JogaAi_Sprint3.pdf")