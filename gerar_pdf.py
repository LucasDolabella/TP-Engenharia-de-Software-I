from fpdf import FPDF

FONT_R = "/System/Library/Fonts/Supplemental/Arial.ttf"
FONT_B = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"
FONT_I = "/System/Library/Fonts/Supplemental/Arial Italic.ttf"
FONT_MONO = "/System/Library/Fonts/Supplemental/Courier New.ttf"


class PDF(FPDF):
    def __init__(self):
        super().__init__()
        self.add_font("Arial", "",  FONT_R)
        self.add_font("Arial", "B", FONT_B)
        self.add_font("Arial", "I", FONT_I)
        self.add_font("Mono",  "",  FONT_MONO)

    def header(self):
        self.set_font("Arial", "B", 9)
        self.set_text_color(108, 71, 255)
        self.cell(0, 7, "Joga Ai - Sistema de Emprestimo de Jogos | DCC603 - UFMG", align="C")
        self.ln(3)
        self.set_draw_color(108, 71, 255)
        self.set_line_width(0.4)
        self.line(10, self.get_y(), 200, self.get_y())
        self.ln(4)

    def footer(self):
        self.set_y(-12)
        self.set_font("Arial", "I", 8)
        self.set_text_color(150, 150, 150)
        self.cell(0, 8, f"Pagina {self.page_no()}", align="C")

    def titulo(self, texto):
        self.ln(3)
        self.set_font("Arial", "B", 14)
        self.set_text_color(108, 71, 255)
        self.cell(0, 8, texto)
        self.ln(2)
        self.set_draw_color(180, 165, 255)
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

    def sub2(self, texto):
        self.ln(1)
        self.set_font("Arial", "B", 10)
        self.set_text_color(80, 80, 80)
        self.cell(0, 6, texto)
        self.ln(4)
        self.set_text_color(30, 30, 30)

    def corpo(self, texto):
        self.set_font("Arial", "", 10)
        self.set_text_color(40, 40, 40)
        self.multi_cell(0, 5.5, texto)
        self.ln(2)

    def codigo(self, texto):
        self.set_font("Mono", "", 8.5)
        self.set_fill_color(245, 245, 252)
        self.set_text_color(30, 30, 80)
        self.multi_cell(0, 4.8, texto, fill=True)
        self.set_font("Arial", "", 10)
        self.set_text_color(40, 40, 40)
        self.ln(2)

    def bullet(self, texto):
        self.set_x(self.l_margin)
        self.set_font("Arial", "", 10)
        self.set_text_color(40, 40, 40)
        self.multi_cell(0, 5.5, "- " + texto)

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

    def caixa_info(self, texto):
        self.set_fill_color(235, 230, 255)
        self.set_font("Arial", "", 9.5)
        self.set_text_color(60, 40, 120)
        self.multi_cell(0, 5.5, texto, fill=True)
        self.set_text_color(30, 30, 30)
        self.ln(2)


# ─────────────────────────────────────────────────────────────────────────────
pdf = PDF()
pdf.set_auto_page_break(auto=True, margin=15)

# ══════════════════════════════════════════════════════════════════════════════
# CAPA
# ══════════════════════════════════════════════════════════════════════════════
pdf.add_page()
pdf.ln(18)
pdf.set_font("Arial", "B", 30)
pdf.set_text_color(108, 71, 255)
pdf.cell(0, 14, "Joga Ai", align="C"); pdf.ln(10)
pdf.set_font("Arial", "B", 17)
pdf.set_text_color(55, 55, 55)
pdf.cell(0, 10, "Sistema de Emprestimo de Jogos de Tabuleiro", align="C"); pdf.ln(8)
pdf.set_font("Arial", "", 11)
pdf.set_text_color(110, 110, 110)
pdf.cell(0, 7, "Sprint 3 - Documentacao Tecnica Completa", align="C"); pdf.ln(14)
pdf.set_draw_color(200, 190, 255)
pdf.set_line_width(0.5)
pdf.line(40, pdf.get_y(), 170, pdf.get_y())
pdf.ln(10)
pdf.set_font("Arial", "", 10)
pdf.set_text_color(70, 70, 70)
for chave, valor in [
    ("Disciplina",   "DCC603 - Engenharia de Software I"),
    ("Instituicao",  "Universidade Federal de Minas Gerais (UFMG)"),
    ("Professor",    "Eduardo Figueiredo"),
    ("Tema",         "11 - Sistema de Controle de Emprestimo de Jogos"),
    ("Equipe",       "Alvaro Lima, Beatriz Nogueira, Lucas Dolabella,"),
    ("",             "Sarah Menks, Vanessa Nascimento"),
    ("Entrega",      "10/06/2026"),
]:
    if chave:
        pdf.set_font("Arial", "B", 10); pdf.cell(32, 7, chave + ":")
    else:
        pdf.cell(32, 7, "")
    pdf.set_font("Arial", "", 10); pdf.cell(0, 7, valor); pdf.ln()

# ══════════════════════════════════════════════════════════════════════════════
# SUMARIO
# ══════════════════════════════════════════════════════════════════════════════
pdf.add_page()
pdf.titulo("Sumario")
itens = [
    ("1.", "Visao Geral do Sistema"),
    ("2.", "Tecnologias Utilizadas"),
    ("3.", "Instalacao e Execucao"),
    ("4.", "Arquitetura do Sistema"),
    ("5.", "Classes OOP - Implementacao do Diagrama de Classes"),
    ("6.", "API REST - Endpoints"),
    ("7.", "Banco de Dados"),
    ("8.", "Frontend - SPA"),
    ("9.", "Fluxos Principais"),
    ("10.", "Requisitos Implementados"),
    ("11.", "Testes de Software"),
    ("12.", "Sistemas Externos"),
    ("13.", "Consideracoes Finais"),
]
for num, texto in itens:
    pdf.set_font("Arial", "B", 10)
    pdf.set_text_color(108, 71, 255)
    pdf.cell(12, 7, num)
    pdf.set_font("Arial", "", 10)
    pdf.set_text_color(30, 30, 30)
    pdf.cell(0, 7, texto)
    pdf.ln()

# ══════════════════════════════════════════════════════════════════════════════
# 1. VISAO GERAL
# ══════════════════════════════════════════════════════════════════════════════
pdf.add_page()
pdf.titulo("1. Visao Geral do Sistema")
pdf.corpo(
    "O Joga Ai e uma plataforma web que conecta pessoas interessadas em emprestar e pegar "
    "emprestados jogos fisicos, como jogos de tabuleiro e cartas. Desenvolvido como trabalho "
    "pratico da disciplina DCC603 - Engenharia de Software I (UFMG), o sistema segue o "
    "processo agil SCRUM com desenvolvimento incremental ao longo de 3 sprints."
)
pdf.corpo(
    "O usuario se cadastra, registra seus jogos disponiveis, pesquisa jogos de outros "
    "usuarios, negocia prazos via chat interno e gerencia o ciclo completo do emprestimo, "
    "incluindo confirmacao de devolucao, aplicacao automatica de penalidades por atraso "
    "(R$ 5,00 por dia) e desbloqueio da conta apos pagamento de multa."
)

pdf.subtitulo("1.1 Objetivos por Sprint")
pdf.tabela(
    ["Sprint", "Objetivo", "Entrega"],
    [
        ["Sprint 1", "Planejamento e especificacao de requisitos (RF/RNF, casos de uso)", "01/04/2026"],
        ["Sprint 2", "Arquitetura em camadas, diagrama de classes, diagramas UML", "27/04/2026"],
        ["Sprint 3", "Implementacao completa, testes unitarios e de integracao", "10/06/2026"],
    ],
    [22, 130, 38]
)

pdf.subtitulo("1.2 Atores do Sistema")
pdf.tabela(
    ["Ator", "Tipo", "Responsabilidades"],
    [
        ["Usuario", "Principal", "Cadastrar, logar, gerenciar jogos, solicitar emprestimos, usar chat"],
        ["Sistema de E-mail", "Externo", "Enviar notificacoes de prazo vencido e comprovantes"],
        ["Sistema de Pagamento", "Externo", "Processar pagamento de multas por atraso"],
    ],
    [35, 22, 133]
)

# ══════════════════════════════════════════════════════════════════════════════
# 2. TECNOLOGIAS
# ══════════════════════════════════════════════════════════════════════════════
pdf.titulo("2. Tecnologias Utilizadas")
pdf.tabela(
    ["Componente", "Tecnologia", "Versao", "Justificativa"],
    [
        ["Backend",         "Python + Flask",        "3.x / 3.0.3",  "OOP nativo, modular, REST simples"],
        ["ORM",             "Flask-SQLAlchemy",       "3.1.1",        "Mapeamento OOP, migracao facil de BD"],
        ["Banco de Dados",  "SQLite",                 "embutido",     "Zero setup, arquivo unico, ideal para TP"],
        ["Autenticacao",    "PyJWT",                  "2.8.0",        "Tokens stateless, ideal para APIs REST"],
        ["Seguranca",       "Werkzeug (bcrypt)",      "3.0.3",        "Hash seguro de senhas, embutido no Flask"],
        ["Testes",          "pytest",                 "9.x",          "Equivalente ao JUnit, padrao Python"],
        ["Frontend",        "HTML5 + CSS3 + JS",      "vanilla",      "SPA sem dependencias, sem build step"],
    ],
    [32, 42, 22, 94]
)

pdf.subtitulo("2.1 Dependencias (requirements.txt)")
pdf.codigo(
    "Flask==3.0.3\n"
    "Flask-SQLAlchemy==3.1.1\n"
    "PyJWT==2.8.0\n"
    "Werkzeug==3.0.3\n"
    "pytest==9.x           # somente para testes"
)

# ══════════════════════════════════════════════════════════════════════════════
# 3. INSTALACAO E EXECUCAO
# ══════════════════════════════════════════════════════════════════════════════
pdf.add_page()
pdf.titulo("3. Instalacao e Execucao")

pdf.subtitulo("3.1 Requisitos")
pdf.bullet("Python 3.10 ou superior")
pdf.bullet("pip (gerenciador de pacotes Python)")
pdf.ln(3)

pdf.subtitulo("3.2 Passos para executar")
pdf.codigo(
    "# 1. Clonar o repositorio\n"
    "git clone <url-do-repositorio>\n"
    "cd TP-Engenharia-de-Software-I\n\n"
    "# 2. Criar e ativar ambiente virtual\n"
    "python3 -m venv venv\n"
    "source venv/bin/activate          # macOS / Linux\n"
    "# venv\\Scripts\\activate          # Windows\n\n"
    "# 3. Instalar dependencias\n"
    "pip install -r requirements.txt\n\n"
    "# 4. Iniciar o servidor\n"
    "python run.py\n\n"
    "# 5. Abrir no navegador\n"
    "# http://localhost:5000\n\n"
    "# Para parar o servidor: Ctrl + C"
)

pdf.caixa_info(
    "O banco de dados SQLite e criado automaticamente em instance/jogaai.db na primeira "
    "execucao. Nao e necessario nenhuma configuracao adicional de banco de dados."
)

# ══════════════════════════════════════════════════════════════════════════════
# 4. ARQUITETURA
# ══════════════════════════════════════════════════════════════════════════════
pdf.add_page()
pdf.titulo("4. Arquitetura do Sistema")
pdf.corpo(
    "O sistema adota a Arquitetura em Camadas (Layered Architecture), definida na Sprint 2, "
    "organizada em cinco camadas hierarquicas com responsabilidades bem separadas. Cada "
    "camada so se comunica com a camada imediatamente inferior, garantindo baixo acoplamento."
)

pdf.subtitulo("4.1 Diagrama de Camadas")
pdf.codigo(
    "+--------------------------------------------------+\n"
    "|  APRESENTACAO  (templates/ + static/)            |\n"
    "|  SPA: HTML, CSS, JavaScript vanilla              |\n"
    "+--------------------+-----------------------------+\n"
    "                     | HTTP / JSON\n"
    "+--------------------v-----------------------------+\n"
    "|  APLICACAO  (app/routes/)                        |\n"
    "|  API REST - 6 blueprints Flask                   |\n"
    "+--------------------+-----------------------------+\n"
    "                     | chamadas de metodo\n"
    "+--------------------v-----------------------------+\n"
    "|  NEGOCIO  (app/models/ + app/services/)          |\n"
    "|  6 classes OOP + 5 servicos                      |\n"
    "+--------------------+-----------------------------+\n"
    "                     | SQLAlchemy ORM\n"
    "+--------------------v-----------------------------+\n"
    "|  DADOS  (SQLite - instance/jogaai.db)             |\n"
    "+--------------------+-----------------------------+\n"
    "                     |\n"
    "+--------------------v-----------------------------+\n"
    "|  SISTEMAS EXTERNOS  (app/external/)              |\n"
    "|  EmailService + PaymentService (stubs)           |\n"
    "+--------------------------------------------------+"
)

pdf.subtitulo("4.2 Camadas e Correspondencia com o Codigo")
pdf.tabela(
    ["Camada", "Diretorio", "Responsabilidade"],
    [
        ["Apresentacao", "templates/ + static/", "Frontend SPA: HTML, CSS, JavaScript"],
        ["Aplicacao",    "app/routes/",           "API REST: recebe req., valida, repassa"],
        ["Negocio",      "app/models/ + services/","Classes OOP + regras de negocio"],
        ["Dados",        "app/database.py + SQLite","Persistencia via SQLAlchemy ORM"],
        ["Ext. Sistemas","app/external/",          "E-mail e pagamento (stubs integraveis)"],
    ],
    [35, 55, 100]
)

pdf.subtitulo("4.3 Estrutura de Diretorios")
pdf.codigo(
    "TP-Engenharia-de-Software-I/\n"
    "|- run.py                       # Ponto de entrada\n"
    "|- requirements.txt             # Flask, SQLAlchemy, PyJWT, Werkzeug\n"
    "|- app/\n"
    "|  |- __init__.py               # App factory (create_app)\n"
    "|  |- database.py               # Instancia SQLAlchemy\n"
    "|  |- models/                   # Camada de Negocio - Classes OOP\n"
    "|  |  |- usuario.py             # Usuario + StatusUsuario\n"
    "|  |  |- jogo.py                # Jogo + StatusJogo\n"
    "|  |  |- emprestimo.py          # Emprestimo + StatusEmprestimo\n"
    "|  |  |- mensagem.py            # Mensagem (chat)\n"
    "|  |  |- notificacao.py         # Notificacao + TipoNotificacao\n"
    "|  |  |- penalidade.py          # Penalidade + StatusPenalidade\n"
    "|  |- services/                 # Camada de Aplicacao\n"
    "|  |  |- auth_service.py        # Registro, login, JWT\n"
    "|  |  |- jogo_service.py        # CRUD de jogos, busca\n"
    "|  |  |- emprestimo_service.py  # Solicitar, confirmar, penalizar\n"
    "|  |  |- chat_service.py        # Envio e listagem de mensagens\n"
    "|  |  |- penalidade_service.py  # Processamento de pagamento\n"
    "|  |- routes/                   # Camada de Apresentacao (API)\n"
    "|  |  |- middleware.py          # requer_autenticacao (JWT)\n"
    "|  |  |- auth.py, jogos.py, emprestimos.py\n"
    "|  |  |- chat.py, penalidades.py, notificacoes.py\n"
    "|  |- external/\n"
    "|     |- email_service.py       # Stub de e-mail\n"
    "|     |- payment_service.py     # Stub de pagamento\n"
    "|- templates/index.html         # SPA principal\n"
    "|- static/css/style.css\n"
    "|- static/js/  (api, auth, jogos, emprestimos, chat, app).js\n"
    "|- tests/\n"
    "   |- conftest.py               # Fixtures pytest\n"
    "   |- test_unitario.py          # 35 testes unitarios\n"
    "   |- test_integracao.py        # 31 testes de integracao"
)

# ══════════════════════════════════════════════════════════════════════════════
# 5. CLASSES OOP
# ══════════════════════════════════════════════════════════════════════════════
pdf.add_page()
pdf.titulo("5. Classes OOP - Implementacao do Diagrama de Classes")
pdf.corpo(
    "As seis classes principais foram implementadas diretamente a partir do Diagrama de "
    "Classes definido na Sprint 2, mantendo atributos, metodos, visibilidades e enumeracoes "
    "identicos ao diagrama UML. Cada classe estende db.Model (SQLAlchemy), unindo "
    "persistencia e comportamento de negocio no mesmo objeto orientado a objetos."
)

pdf.subtitulo("5.1 Usuario  (app/models/usuario.py)")
pdf.tabela(
    ["Membro", "Tipo / Retorno", "Visibilidade", "Descricao"],
    [
        ["id",               "String (UUID)",    "publico",   "Identificador unico gerado automaticamente"],
        ["nome",             "String",           "publico",   "Nome completo do usuario"],
        ["email",            "String (unico)",   "publico",   "E-mail usado no login"],
        ["senha",            "String",           "publico",   "Hash bcrypt da senha"],
        ["status",           "StatusUsuario",    "publico",   "ATIVO / INATIVO / BLOQUEADO"],
        ["avaliacao",        "Float",            "publico",   "Media de avaliacoes recebidas"],
        ["data_cadastro",    "DateTime",         "publico",   "Data de criacao da conta"],
        ["cadastrar()",      "void",             "publico",   "Inicializa usuario com senha hasheada"],
        ["login()",          "bool",             "publico",   "Valida e-mail e senha"],
        ["bloquear()",       "void",             "publico",   "Muda status para BLOQUEADO"],
        ["desbloquear()",    "void",             "publico",   "Muda status para ATIVO"],
        ["atualizar_perfil()","void",            "publico",   "Atualiza nome ou senha"],
        ["esta_bloqueado()", "bool",             "publico",   "Retorna true se status = BLOQUEADO"],
        ["_validar_senha()", "bool",             "privado",   "Verifica hash bcrypt da senha"],
    ],
    [42, 32, 24, 92]
)

pdf.subtitulo("5.2 Jogo  (app/models/jogo.py)")
pdf.tabela(
    ["Membro", "Tipo / Retorno", "Visibilidade", "Descricao"],
    [
        ["id",                     "String (UUID)", "publico", "Identificador unico"],
        ["nome",                   "String",        "publico", "Nome do jogo"],
        ["descricao",              "Text",          "publico", "Descricao completa"],
        ["categoria",              "String",        "publico", "Ex: Estrategia, Cartas, RPG"],
        ["status",                 "StatusJogo",    "publico", "DISPONIVEL / EMPRESTADO"],
        ["dono_id",                "FK -> Usuario", "publico", "Dono do jogo"],
        ["cadastrar()",            "void",          "publico", "Valida e inicializa o jogo"],
        ["verificar_disponibilidade()","bool",      "publico", "True se status = DISPONIVEL"],
        ["atualizar_status()",     "void",          "publico", "Muda o status do jogo"],
        ["buscar(termo)",          "List[Jogo]",    "publico", "Busca por nome ou categoria (estatico)"],
        ["listar_por_categoria()","List[Jogo]",     "publico", "Filtra por categoria (estatico)"],
        ["_validar_dados()",       "bool",          "privado", "Valida campos obrigatorios"],
    ],
    [50, 32, 24, 84]
)

pdf.add_page()
pdf.subtitulo("5.3 Emprestimo  (app/models/emprestimo.py)")
pdf.tabela(
    ["Membro", "Tipo / Retorno", "Visibilidade", "Descricao"],
    [
        ["id",                    "String (UUID)",    "publico", "Identificador unico"],
        ["dono_id",               "FK -> Usuario",    "publico", "Dono do jogo emprestado"],
        ["solicitante_id",        "FK -> Usuario",    "publico", "Quem pegou emprestado"],
        ["jogo_id",               "FK -> Jogo",       "publico", "Jogo em questao"],
        ["status",                "StatusEmprestimo", "publico", "ATIVO / DEVOLVIDO / CANCELADO"],
        ["data_inicio",           "DateTime",         "publico", "Data da solicitacao"],
        ["data_prazo",            "DateTime",         "publico", "Prazo acordado para devolucao"],
        ["data_devolvido",        "DateTime",         "publico", "Data real de devolucao (nullable)"],
        ["solicitar()",           "void",             "publico", "Valida e registra o emprestimo"],
        ["confirmar_devolucao()", "void",             "publico", "Marca DEVOLVIDO e libera o jogo"],
        ["cancelar()",            "void",             "publico", "Cancela e libera o jogo"],
        ["verificar_atraso()",    "bool",             "publico", "True se agora > data_prazo e ATIVO"],
        ["calcular_dias_atraso()","int",              "publico", "Dias entre prazo e hoje (0 se no prazo)"],
        ["atualizar_status()",    "void",             "publico", "Muda o status do emprestimo"],
        ["_validar_solicitacao()","bool",             "privado", "Verifica bloqueio, disponib., dono"],
    ],
    [50, 32, 24, 84]
)

pdf.subtitulo("5.4 Mensagem  (app/models/mensagem.py)")
pdf.tabela(
    ["Membro", "Tipo / Retorno", "Visibilidade", "Descricao"],
    [
        ["id",                      "String (UUID)", "publico", "Identificador unico"],
        ["remetente_id",            "FK -> Usuario", "publico", "Quem enviou"],
        ["destinatario_id",         "FK -> Usuario", "publico", "Quem recebe"],
        ["emprestimo_id",           "FK -> Emprestimo","publico","Chat vinculado ao emprestimo"],
        ["conteudo",                "Text",          "publico", "Texto da mensagem"],
        ["lida",                    "Boolean",       "publico", "Se o destinatario ja leu"],
        ["data_envio",              "DateTime",      "publico", "Momento do envio"],
        ["enviar()",                "void",          "publico", "Valida e prepara a mensagem"],
        ["marcar_como_lida()",      "void",          "publico", "Muda lida = True"],
        ["listar_por_emprestimo()", "List[Mensagem]","publico", "Historico ordenado por data (estatico)"],
        ["_validar_conteudo()",     "bool",          "privado", "Impede mensagem vazia"],
    ],
    [50, 32, 24, 84]
)

pdf.add_page()
pdf.subtitulo("5.5 Notificacao  (app/models/notificacao.py)")
pdf.tabela(
    ["Membro", "Tipo / Retorno", "Visibilidade", "Descricao"],
    [
        ["id",              "String (UUID)",   "publico", "Identificador unico"],
        ["destinatario_id", "FK -> Usuario",   "publico", "Quem recebe a notificacao"],
        ["mensagem",        "Text",            "publico", "Texto gerado automaticamente pelo tipo"],
        ["tipo",            "TipoNotificacao", "publico", "SOLICITACAO_EMPRESTIMO / PRAZO_VENCIDO /"],
        ["",                "",               "",        "DEVOLUCAO_CONFIRMADA / NOVA_MENSAGEM /"],
        ["",                "",               "",        "PENALIDADE_APLICADA"],
        ["lida",            "Boolean",         "publico", "Se o usuario ja visualizou"],
        ["data_envio",      "DateTime",        "publico", "Momento do envio"],
        ["emprestimo_id",   "FK -> Emprestimo","publico", "Emprestimo relacionado (opcional)"],
        ["enviar()",        "void",            "publico", "Inicializa e gera a mensagem pelo tipo"],
        ["marcar_como_lida()","void",          "publico", "Muda lida = True"],
        ["listar_por_usuario()","List",        "publico", "Retorna notificacoes do usuario (estatico)"],
        ["_gerar_mensagem()","str",            "privado", "Texto descritivo por tipo de notificacao"],
    ],
    [50, 32, 24, 84]
)

pdf.subtitulo("5.6 Penalidade  (app/models/penalidade.py)")
pdf.tabela(
    ["Membro", "Tipo / Retorno", "Visibilidade", "Descricao"],
    [
        ["id",                  "String (UUID)",    "publico", "Identificador unico"],
        ["usuario_id",          "FK -> Usuario",    "publico", "Quem recebeu a penalidade"],
        ["emprestimo_id",       "FK -> Emprestimo", "publico", "Emprestimo em atraso"],
        ["valor_multa",         "Float",            "publico", "R$ 5,00 * dias_atraso (minimo R$ 5)"],
        ["status",              "StatusPenalidade", "publico", "PENDENTE / PAGA / CANCELADA"],
        ["data_aplicacao",      "DateTime",         "publico", "Quando a penalidade foi gerada"],
        ["data_pagamento",      "DateTime",         "publico", "Quando foi quitada (nullable)"],
        ["aplicar()",           "void",             "publico", "Calcula multa e bloqueia o usuario"],
        ["confirmar_pagamento()","void",            "publico", "Marca PAGA e desbloqueia o usuario"],
        ["desbloquear_usuario()","void",            "publico", "Chama usuario.desbloquear()"],
        ["listar_por_usuario()", "List",            "publico", "Penalidades do usuario (estatico)"],
        ["_calcular_multa()",   "float",            "privado", "dias_atraso x R$5 (minimo R$5)"],
        ["_bloquear_usuario()", "void",             "privado", "Chama usuario.bloquear()"],
    ],
    [50, 32, 24, 84]
)

# ══════════════════════════════════════════════════════════════════════════════
# 6. API REST
# ══════════════════════════════════════════════════════════════════════════════
pdf.add_page()
pdf.titulo("6. API REST - Endpoints")
pdf.caixa_info("Todas as rotas marcadas como 'Sim' em autenticacao exigem o header:\nAuthorization: Bearer <token_jwt>")

pdf.subtitulo("6.1 Autenticacao  /api/auth")
pdf.tabela(
    ["Metodo", "Rota", "Auth", "Descricao"],
    [
        ["POST", "/api/auth/cadastrar",  "Nao", "Cria conta, retorna JWT + dados do usuario"],
        ["POST", "/api/auth/login",      "Nao", "Login com e-mail e senha, retorna JWT"],
        ["GET",  "/api/auth/perfil",     "Sim", "Retorna dados do usuario autenticado"],
        ["PUT",  "/api/auth/perfil",     "Sim", "Atualiza nome ou senha"],
    ],
    [18, 62, 14, 96]
)

pdf.subtitulo("6.2 Jogos  /api/jogos")
pdf.tabela(
    ["Metodo", "Rota", "Auth", "Descricao"],
    [
        ["GET",    "/api/jogos",          "Nao", "Lista jogos (aceita ?busca=termo para filtrar)"],
        ["GET",    "/api/jogos/meus",     "Sim", "Lista jogos do usuario autenticado"],
        ["GET",    "/api/jogos/:id",      "Nao", "Detalhe de um jogo especifico"],
        ["POST",   "/api/jogos",          "Sim", "Cadastra novo jogo"],
        ["PUT",    "/api/jogos/:id",      "Sim", "Atualiza jogo (somente o dono)"],
        ["DELETE", "/api/jogos/:id",      "Sim", "Remove jogo (somente dono, se disponivel)"],
    ],
    [18, 62, 14, 96]
)

pdf.subtitulo("6.3 Emprestimos  /api/emprestimos")
pdf.tabela(
    ["Metodo", "Rota", "Auth", "Descricao"],
    [
        ["GET", "/api/emprestimos",                          "Sim", "Lista emprestimos do usuario (dono ou solicitante)"],
        ["GET", "/api/emprestimos/:id",                      "Sim", "Detalhe de um emprestimo"],
        ["POST","/api/emprestimos",                          "Sim", "Solicita emprestimo (jogo_id, data_prazo)"],
        ["PUT", "/api/emprestimos/:id/confirmar-devolucao",  "Sim", "Dono confirma que jogo foi devolvido"],
        ["PUT", "/api/emprestimos/:id/nao-devolvido",        "Sim", "Dono reporta nao devolucao -> penalidade"],
        ["PUT", "/api/emprestimos/:id/cancelar",             "Sim", "Cancela emprestimo ativo"],
    ],
    [18, 78, 14, 80]
)

pdf.subtitulo("6.4 Chat, Penalidades e Notificacoes")
pdf.tabela(
    ["Metodo", "Rota", "Auth", "Descricao"],
    [
        ["GET",  "/api/chat/:id",                      "Sim", "Lista mensagens (marca nao lidas como lidas)"],
        ["POST", "/api/chat/:id",                      "Sim", "Envia mensagem no chat"],
        ["GET",  "/api/penalidades",                   "Sim", "Lista penalidades do usuario"],
        ["POST", "/api/penalidades/:id/pagar",         "Sim", "Paga multa e desbloqueia a conta"],
        ["GET",  "/api/notificacoes",                  "Sim", "Lista notificacoes do usuario"],
        ["PUT",  "/api/notificacoes/:id/lida",         "Sim", "Marca notificacao como lida"],
        ["PUT",  "/api/notificacoes/marcar-todas-lidas","Sim","Marca todas as notificacoes como lidas"],
    ],
    [18, 78, 14, 80]
)

pdf.add_page()
pdf.subtitulo("6.5 Exemplos de Requisicao")
pdf.sub2("Cadastrar usuario:")
pdf.codigo(
    'curl -X POST http://localhost:5000/api/auth/cadastrar \\\n'
    '  -H "Content-Type: application/json" \\\n'
    '  -d \'{"nome": "Lucas", "email": "lucas@email.com", "senha": "minhasenha"}\''
)
pdf.sub2("Cadastrar jogo (com token):")
pdf.codigo(
    'curl -X POST http://localhost:5000/api/jogos \\\n'
    '  -H "Authorization: Bearer <token>" \\\n'
    '  -H "Content-Type: application/json" \\\n'
    '  -d \'{"nome": "Catan", "descricao": "Jogo de estrategia", "categoria": "Estrategia"}\''
)
pdf.sub2("Solicitar emprestimo:")
pdf.codigo(
    'curl -X POST http://localhost:5000/api/emprestimos \\\n'
    '  -H "Authorization: Bearer <token>" \\\n'
    '  -H "Content-Type: application/json" \\\n'
    '  -d \'{"jogo_id": "<id>", "data_prazo": "2026-06-20T23:59:59"}\''
)

# ══════════════════════════════════════════════════════════════════════════════
# 7. BANCO DE DADOS
# ══════════════════════════════════════════════════════════════════════════════
pdf.add_page()
pdf.titulo("7. Banco de Dados")
pdf.corpo(
    "O banco de dados e o SQLite, armazenado em instance/jogaai.db e criado automaticamente "
    "pelo SQLAlchemy (db.create_all()) na primeira execucao. O schema reflete diretamente "
    "as 6 classes do diagrama de classes."
)

pdf.subtitulo("7.1 Schema das Tabelas")
pdf.tabela(
    ["Tabela", "Colunas principais", "Relacionamentos"],
    [
        ["usuarios",    "id, nome, email, senha, status, avaliacao, data_cadastro",      "1:N jogos, emprestimos, penalidades"],
        ["jogos",       "id, nome, descricao, categoria, status, dono_id, data_cadastro","N:1 usuarios, 1:N emprestimos"],
        ["emprestimos", "id, dono_id, solicitante_id, jogo_id, status, datas",           "N:1 usuarios/jogos, 1:N mensagens"],
        ["mensagens",   "id, remetente_id, destinatario_id, emprestimo_id, conteudo, lida","N:1 usuarios/emprestimos"],
        ["notificacoes","id, destinatario_id, mensagem, tipo, lida, emprestimo_id",       "N:1 usuarios/emprestimos"],
        ["penalidades", "id, usuario_id, emprestimo_id, valor_multa, status, datas",     "N:1 usuarios/emprestimos"],
    ],
    [28, 90, 72]
)

pdf.subtitulo("7.2 Visualizar os Dados")
pdf.codigo(
    "# Instalar DB Browser for SQLite (macOS)\n"
    "brew install db-browser-for-sqlite\n"
    "open -a 'DB Browser for SQLite'\n"
    "# Abrir: instance/jogaai.db\n\n"
    "# Ou via terminal\n"
    "sqlite3 instance/jogaai.db\n"
    ".tables\n"
    "SELECT * FROM usuarios;\n"
    "SELECT * FROM emprestimos WHERE status = 'ATIVO';\n"
    "SELECT * FROM penalidades WHERE status = 'PENDENTE';\n"
    ".quit"
)

# ══════════════════════════════════════════════════════════════════════════════
# 8. FRONTEND
# ══════════════════════════════════════════════════════════════════════════════
pdf.titulo("8. Frontend - SPA (Single Page Application)")
pdf.corpo(
    "O frontend e uma SPA construida com HTML, CSS e JavaScript puro (vanilla), sem "
    "frameworks externos. Todas as telas sao renderizadas dinamicamente por JavaScript "
    "no mesmo arquivo index.html. O roteamento e feito pelo app.js que mostra/oculta "
    "as views conforme a navegacao."
)

pdf.subtitulo("8.1 Telas Implementadas")
pdf.tabela(
    ["Tela", "Arquivo JS", "Funcionalidades"],
    [
        ["Login / Cadastro",  "auth.js",         "Formularios, validacao, armazena JWT no localStorage"],
        ["Explorar Jogos",    "jogos.js (Jogos)", "Grid de jogos, busca em tempo real (debounce 300ms)"],
        ["Meus Jogos",        "jogos.js (MeusJogos)","CRUD: adicionar, editar, remover jogos proprios"],
        ["Emprestimos",       "emprestimos.js",  "Lista ativa, historico, acoes por papel (dono/sol.)"],
        ["Chat",              "chat.js",         "Mensagens com auto-refresh a cada 4 segundos"],
        ["Penalidades",       "emprestimos.js",  "Visualizar multas pendentes, pagar com um clique"],
        ["Notificacoes",      "emprestimos.js",  "Centro de notificacoes, badge com contador no navbar"],
    ],
    [38, 42, 110]
)

pdf.subtitulo("8.2 Fluxo de Autenticacao no Frontend")
pdf.corpo(
    "Apos login/cadastro bem-sucedido, o token JWT e salvo no localStorage do navegador. "
    "O objeto Api (api.js) injeta automaticamente o header Authorization: Bearer <token> "
    "em todas as requisicoes autenticadas. No logout, o token e os dados do usuario sao "
    "removidos do localStorage."
)

# ══════════════════════════════════════════════════════════════════════════════
# 9. FLUXOS PRINCIPAIS
# ══════════════════════════════════════════════════════════════════════════════
pdf.add_page()
pdf.titulo("9. Fluxos Principais")

pdf.subtitulo("9.1 Fluxo de Emprestimo (Cenario 1 - Sprint 2)")
pdf.tabela(
    ["Passo", "Ator", "Acao do Sistema"],
    [
        ["1",  "Solicitante", "Busca e seleciona jogo disponivel na tela Explorar"],
        ["2",  "Solicitante", "Clica em 'Pegar Emprestado' e define prazo de devolucao"],
        ["3",  "Sistema",     "Valida: usuario nao bloqueado, jogo disponivel, nao e o proprio dono"],
        ["4",  "Sistema",     "Cria Emprestimo (ATIVO), muda Jogo para EMPRESTADO"],
        ["5",  "Sistema",     "Cria Notificacao SOLICITACAO_EMPRESTIMO para o dono"],
        ["6",  "Ambos",       "Trocam mensagens via Chat (auto-refresh a cada 4s)"],
        ["7",  "Sistema",     "No vencimento: EmailService.enviar_aviso_prazo_vencido()"],
        ["8a", "Dono",        "Confirma devolucao -> Emprestimo DEVOLVIDO, Jogo DISPONIVEL"],
        ["8b", "Dono",        "Ou reporta nao devolucao -> Penalidade criada, solicitante BLOQUEADO"],
    ],
    [14, 30, 146]
)

pdf.subtitulo("9.2 Fluxo de Penalidade e Pagamento (Cenarios 2 e 4 - Sprint 2)")
pdf.tabela(
    ["Passo", "Ator", "Acao do Sistema"],
    [
        ["1", "Dono",        "Clica em 'Nao Devolvido' no emprestimo atrasado"],
        ["2", "Sistema",     "Penalidade._calcular_multa(): dias_atraso x R$5,00 (min R$5)"],
        ["3", "Sistema",     "Penalidade criada (PENDENTE), usuario.bloquear() chamado"],
        ["4", "Sistema",     "Notificacao PENALIDADE_APLICADA enviada ao solicitante"],
        ["5", "Solicitante", "Acessa 'Penalidades', ve valor e motivo da multa"],
        ["6", "Solicitante", "Clica em 'Pagar Multa' (seleciona metodo de pagamento)"],
        ["7", "Sistema",     "PaymentService.processar(valor, metodo) -> aprovado"],
        ["8", "Sistema",     "Penalidade.confirmar_pagamento(): status PAGA, data registrada"],
        ["9", "Sistema",     "usuario.desbloquear(): status ATIVO"],
        ["10","Sistema",     "EmailService.enviar_comprovante_pagamento() chamado"],
    ],
    [14, 30, 146]
)

pdf.subtitulo("9.3 Fluxo de Chat (Cenario 5 - Sprint 2)")
pdf.tabela(
    ["Passo", "Ator", "Acao do Sistema"],
    [
        ["1", "Solicitante/Dono","Clica em 'Chat' no emprestimo ATIVO na tela de Emprestimos"],
        ["2", "Sistema",        "Verifica se usuario e dono ou solicitante do emprestimo"],
        ["3", "Sistema",        "Abre interface de chat com historico carregado"],
        ["4", "Usuario",        "Digita e envia mensagem"],
        ["5", "Sistema",        "Mensagem validada (nao vazia), salva no BD"],
        ["6", "Sistema",        "Cria Notificacao NOVA_MENSAGEM para o destinatario"],
        ["7", "Destinatario",   "Recebe mensagem via auto-refresh (polling 4s)"],
    ],
    [14, 30, 146]
)

# ══════════════════════════════════════════════════════════════════════════════
# 10. REQUISITOS
# ══════════════════════════════════════════════════════════════════════════════
pdf.add_page()
pdf.titulo("10. Requisitos Implementados")

pdf.subtitulo("10.1 Requisitos Funcionais")
pdf.tabela(
    ["RF", "Descricao", "Prioridade", "Status"],
    [
        ["RF01", "Cadastro de usuarios (nome, e-mail, senha)",        "Alta",  "Implementado"],
        ["RF02", "Login / Logout com autenticacao JWT",               "Alta",  "Implementado"],
        ["RF03", "Cadastrar jogos disponiveis para emprestimo",       "Alta",  "Implementado"],
        ["RF04", "Visualizar jogos disponiveis na plataforma",        "Alta",  "Implementado"],
        ["RF05", "Busca de jogos por nome ou categoria",              "Alta",  "Implementado"],
        ["RF06", "Solicitar emprestimo de um jogo disponivel",        "Alta",  "Implementado"],
        ["RF07", "Definir prazo de devolucao no momento da solicit.", "Alta",  "Implementado"],
        ["RF08", "Registrar todas as informacoes do emprestimo",      "Alta",  "Implementado"],
        ["RF09", "Chat interno vinculado ao emprestimo",              "Baixa", "Implementado"],
        ["RF10", "E-mail ao dono no vencimento do prazo",             "Baixa", "Stub"],
        ["RF11", "Dono do jogo confirma devolucao",                   "Alta",  "Implementado"],
        ["RF12", "Bloquear usuario inadimplente",                     "Alta",  "Implementado"],
        ["RF13", "Aplicar multa por atraso (R$ 5,00/dia)",           "Media", "Implementado"],
        ["RF14", "Desbloquear conta apos pagamento da multa",         "Media", "Implementado"],
        ["RF17", "Indicar status do jogo (disponivel/emprestado)",    "Alta",  "Implementado"],
        ["RF18", "Cancelar solicitacao de emprestimo",                "Media", "Implementado"],
        ["RF19", "Notificacoes internas no sistema",                  "Baixa", "Implementado"],
    ],
    [15, 112, 22, 41]
)

pdf.subtitulo("10.2 Requisitos Nao Funcionais Atendidos")
pdf.tabela(
    ["RNF", "Descricao", "Como foi atendido"],
    [
        ["RNF01", "Facilidade de uso",       "SPA intuitiva, sem treinamento previo"],
        ["RNF05", "Protecao de dados",       "JWT + bcrypt, rotas protegidas"],
        ["RNF06", "Criptografia de senha",   "Werkzeug generate_password_hash (bcrypt)"],
        ["RNF07", "Autenticacao restrita",   "Middleware requer_autenticacao em todas as rotas"],
        ["RNF08", "Integridade dos dados",   "Transacoes SQLAlchemy + FK constraints"],
        ["RNF09", "Consistencia de estados", "Jogo nao pode ser DISPONIVEL e EMPRESTADO simultaneamente"],
        ["RNF12", "Manutenibilidade",        "Arquitetura em camadas, modulos independentes"],
        ["RNF13", "Acesso multiplataforma",  "Aplicacao web, qualquer navegador moderno"],
    ],
    [16, 48, 126]
)

# ══════════════════════════════════════════════════════════════════════════════
# 11. TESTES
# ══════════════════════════════════════════════════════════════════════════════
pdf.add_page()
pdf.titulo("11. Testes de Software")
pdf.corpo(
    "O projeto possui 66 testes automatizados divididos em duas suites: testes unitarios "
    "e testes de integracao. Os testes usam pytest (equivalente ao JUnit para Python) e "
    "um banco SQLite em memoria (isolado por teste), garantindo que cada teste comece "
    "com um banco limpo e sem efeitos colaterais entre eles."
)

pdf.subtitulo("11.1 Como Executar os Testes")
pdf.codigo(
    "# Ativar o ambiente virtual\n"
    "source venv/bin/activate\n\n"
    "# Executar todos os testes\n"
    "python -m pytest tests/ -v\n\n"
    "# Executar apenas testes unitarios\n"
    "python -m pytest tests/test_unitario.py -v\n\n"
    "# Executar apenas testes de integracao\n"
    "python -m pytest tests/test_integracao.py -v\n\n"
    "# Resultado esperado: 66 passed"
)

pdf.subtitulo("11.2 Configuracao dos Testes (conftest.py)")
pdf.corpo(
    "O arquivo tests/conftest.py define as fixtures compartilhadas entre todos os testes:"
)
pdf.tabela(
    ["Fixture", "Escopo", "O que fornece"],
    [
        ["app",    "function", "Instancia Flask configurada com banco SQLite em memoria"],
        ["client", "function", "Flask test client para simular requisicoes HTTP"],
        ["db",     "function", "Instancia SQLAlchemy com tabelas criadas do zero"],
    ],
    [20, 20, 150]
)
pdf.corpo(
    "A cada teste, o banco e criado do zero (db.create_all()) e destruido ao final "
    "(db.drop_all()), garantindo isolamento total entre os testes."
)

pdf.add_page()
pdf.subtitulo("11.3 Testes Unitarios  (tests/test_unitario.py) - 35 testes")
pdf.corpo(
    "Testam as regras de negocio das classes isoladamente, sem HTTP nem banco em disco. "
    "Cada metodo de negocio e testado de forma independente."
)

pdf.sub2("TestUsuario (10 testes)")
pdf.tabela(
    ["Teste", "O que verifica"],
    [
        ["test_cadastrar_define_status_ativo",          "Status inicial do usuario e ATIVO apos cadastro"],
        ["test_senha_e_armazenada_como_hash",           "Senha nao e armazenada em texto plano"],
        ["test_validar_senha_correta",                  "_validar_senha() retorna True para senha correta"],
        ["test_validar_senha_incorreta",                "_validar_senha() retorna False para senha errada"],
        ["test_bloquear_muda_status",                   "bloquear() muda status para BLOQUEADO"],
        ["test_desbloquear_muda_status",                "desbloquear() muda status de volta para ATIVO"],
        ["test_esta_bloqueado_retorna_true",            "esta_bloqueado() retorna True quando BLOQUEADO"],
        ["test_esta_bloqueado_retorna_false_quando_ativo","esta_bloqueado() retorna False quando ATIVO"],
        ["test_atualizar_perfil_nome",                  "atualizar_perfil() modifica o nome corretamente"],
        ["test_to_dict_nao_expoe_senha",                "to_dict() nao inclui o campo 'senha'"],
    ],
    [80, 110]
)

pdf.sub2("TestJogo (6 testes)")
pdf.tabela(
    ["Teste", "O que verifica"],
    [
        ["test_cadastrar_define_status_disponivel",             "Status inicial do jogo e DISPONIVEL"],
        ["test_cadastrar_campos_obrigatorios_vazios_levanta_erro","ValueError para campos vazios"],
        ["test_verificar_disponibilidade_true",                 "True quando status = DISPONIVEL"],
        ["test_verificar_disponibilidade_false_quando_emprestado","False quando status = EMPRESTADO"],
        ["test_atualizar_nome_e_categoria",                     "atualizar() modifica os campos corretamente"],
        ["test_to_dict_contem_campos_basicos",                  "to_dict() contem nome e status"],
    ],
    [90, 100]
)

pdf.sub2("TestEmprestimo (9 testes)")
pdf.tabela(
    ["Teste", "O que verifica"],
    [
        ["test_solicitar_cria_emprestimo_ativo",          "Status inicial do emprestimo e ATIVO"],
        ["test_solicitar_usuario_bloqueado_levanta_erro", "ValueError se solicitante estiver bloqueado"],
        ["test_solicitar_jogo_indisponivel_levanta_erro", "ValueError se jogo nao estiver disponivel"],
        ["test_solicitar_proprio_jogo_levanta_erro",      "ValueError se usuario tenta pegar o proprio jogo"],
        ["test_confirmar_devolucao_muda_status",          "Status muda para DEVOLVIDO e jogo fica DISPONIVEL"],
        ["test_cancelar_libera_jogo",                     "Status muda para CANCELADO e jogo fica DISPONIVEL"],
        ["test_verificar_atraso_false_dentro_do_prazo",   "False quando data_prazo esta no futuro"],
        ["test_verificar_atraso_true_prazo_vencido",      "True quando data_prazo ja passou"],
        ["test_calcular_dias_atraso",                     "Retorna numero correto de dias de atraso"],
    ],
    [90, 100]
)

pdf.add_page()
pdf.sub2("TestPenalidade (6 testes)")
pdf.tabela(
    ["Teste", "O que verifica"],
    [
        ["test_aplicar_calcula_valor_multa",              "Valor = dias_atraso x R$5,00"],
        ["test_aplicar_bloqueia_usuario",                 "aplicar() chama usuario.bloquear()"],
        ["test_multa_minima_um_dia",                      "Valor minimo e R$5,00 (1 dia)"],
        ["test_confirmar_pagamento_muda_status_para_paga","Status muda para PAGA apos pagamento"],
        ["test_confirmar_pagamento_desbloqueia_usuario",  "confirmar_pagamento() chama usuario.desbloquear()"],
        ["test_penalidade_inicial_esta_pendente",         "Status inicial da penalidade e PENDENTE"],
    ],
    [90, 100]
)

pdf.sub2("TestMensagem (4 testes)")
pdf.tabela(
    ["Teste", "O que verifica"],
    [
        ["test_conteudo_vazio_levanta_erro",  "ValueError para conteudo vazio ou apenas espacos"],
        ["test_mensagem_inicia_nao_lida",     "Campo 'lida' inicia como False"],
        ["test_marcar_como_lida",             "marcar_como_lida() muda 'lida' para True"],
        ["test_to_dict_contem_campos_basicos","to_dict() contem campos essenciais"],
    ],
    [80, 110]
)

pdf.subtitulo("11.4 Testes de Integracao  (tests/test_integracao.py) - 31 testes")
pdf.corpo(
    "Testam os fluxos completos via API REST usando o Flask test client. Cada suite "
    "cobre um cenario de uso descrito na Sprint 2."
)

pdf.sub2("TestAutenticacao (6 testes)")
pdf.tabela(
    ["Teste", "O que verifica"],
    [
        ["test_cadastro_retorna_token",            "POST /cadastrar retorna 201 e token JWT"],
        ["test_cadastro_email_duplicado_retorna_409","E-mail duplicado retorna HTTP 409"],
        ["test_login_credenciais_corretas",        "POST /login com credenciais validas retorna 200 e token"],
        ["test_login_senha_errada_retorna_401",    "Senha errada retorna HTTP 401"],
        ["test_rota_protegida_sem_token_retorna_401","Acesso sem token retorna HTTP 401"],
        ["test_perfil_retorna_dados_do_usuario",   "GET /perfil retorna dados sem expor senha"],
    ],
    [90, 100]
)

pdf.sub2("TestJogos (7 testes)")
pdf.tabela(
    ["Teste", "O que verifica"],
    [
        ["test_cadastrar_jogo",                     "POST /jogos cria jogo com status DISPONIVEL"],
        ["test_listar_jogos_sem_autenticacao",       "GET /jogos funciona sem autenticacao"],
        ["test_buscar_jogo_por_nome",               "?busca= filtra corretamente por nome"],
        ["test_buscar_jogo_por_categoria",          "?busca= filtra corretamente por categoria"],
        ["test_remover_jogo_proprio",               "DELETE retorna 200 para o dono"],
        ["test_remover_jogo_alheio_retorna_erro",   "DELETE retorna 400 para quem nao e o dono"],
        ["test_meus_jogos_retorna_apenas_do_usuario","GET /meus retorna so jogos do usuario autenticado"],
    ],
    [90, 100]
)

pdf.sub2("TestSolicitarEmprestimo (5 testes)")
pdf.tabela(
    ["Teste", "O que verifica"],
    [
        ["test_solicitar_emprestimo_com_sucesso",     "POST /emprestimos retorna 201 e status ATIVO"],
        ["test_jogo_fica_indisponivel_apos_emprestimo","Jogo muda para EMPRESTADO apos solicitacao"],
        ["test_nao_pode_solicitar_proprio_jogo",      "Retorna 400 ao tentar pegar o proprio jogo"],
        ["test_nao_pode_solicitar_jogo_indisponivel", "Retorna 400 se jogo ja estiver emprestado"],
        ["test_cancelar_emprestimo_libera_jogo",      "Cancelar muda status do jogo para DISPONIVEL"],
    ],
    [90, 100]
)

pdf.add_page()
pdf.sub2("TestConfirmarDevolucao (3 testes)")
pdf.tabela(
    ["Teste", "O que verifica"],
    [
        ["test_dono_confirma_devolucao",                "PUT confirmar-devolucao retorna status DEVOLVIDO"],
        ["test_jogo_disponivel_apos_devolucao",         "Jogo volta para DISPONIVEL apos confirmacao"],
        ["test_solicitante_nao_pode_confirmar_devolucao","Apenas o dono pode confirmar - retorna 400"],
    ],
    [90, 100]
)

pdf.sub2("TestAplicarPenalidade (3 testes)")
pdf.tabela(
    ["Teste", "O que verifica"],
    [
        ["test_nao_devolucao_bloqueia_solicitante",    "nao-devolvido muda status do usuario para BLOQUEADO"],
        ["test_usuario_bloqueado_nao_pode_solicitar",  "Usuario BLOQUEADO recebe 400 ao solicitar emprestimo"],
        ["test_penalidade_criada_com_valor_correto",   "Valor da multa e >= dias_atraso x R$5,00"],
    ],
    [90, 100]
)

pdf.sub2("TestPagamentoMulta (3 testes)")
pdf.tabela(
    ["Teste", "O que verifica"],
    [
        ["test_pagar_multa_desbloqueia_usuario",            "Apos pagar, usuario volta para ATIVO"],
        ["test_pagar_multa_marca_penalidade_como_paga",     "Status da penalidade muda para PAGA"],
        ["test_outro_usuario_nao_pode_pagar_multa_alheia",  "Retorna 400 ao tentar pagar multa de outro usuario"],
    ],
    [90, 100]
)

pdf.sub2("TestChat (4 testes)")
pdf.tabela(
    ["Teste", "O que verifica"],
    [
        ["test_enviar_mensagem_no_chat",      "POST /chat retorna 201 com mensagem criada"],
        ["test_listar_mensagens_do_chat",     "GET /chat retorna lista com todas as mensagens"],
        ["test_mensagem_vazia_retorna_erro",  "Conteudo vazio ou espacos retorna 400"],
        ["test_terceiro_nao_pode_acessar_chat","Usuario fora do emprestimo recebe 400"],
    ],
    [80, 110]
)

pdf.subtitulo("11.5 Resumo dos Resultados")
pdf.tabela(
    ["Suite", "Arquivo", "Total", "Passando", "Tempo aprox."],
    [
        ["Testes Unitarios",    "test_unitario.py",    "35", "35", "~2s"],
        ["Testes de Integracao","test_integracao.py",  "31", "31", "~7s"],
        ["TOTAL",               "-",                   "66", "66", "~9s"],
    ],
    [38, 55, 20, 28, 49]
)

# ══════════════════════════════════════════════════════════════════════════════
# 12. SISTEMAS EXTERNOS
# ══════════════════════════════════════════════════════════════════════════════
pdf.add_page()
pdf.titulo("12. Sistemas Externos (Stubs)")
pdf.corpo(
    "Os sistemas externos foram implementados como stubs que simulam o comportamento "
    "real e registram as operacoes no log. Em producao, substituir o corpo dos metodos "
    "pela integracao real sem alterar nenhuma outra camada do sistema."
)

pdf.subtitulo("12.1 EmailService (app/external/email_service.py)")
pdf.tabela(
    ["Metodo", "Quando e chamado", "Integracao sugerida"],
    [
        ["enviar_aviso_prazo_vencido()",       "Prazo do emprestimo venceu",           "SMTP / SendGrid"],
        ["enviar_confirmacao_devolucao()",     "Dono confirma devolucao",              "SMTP / SendGrid"],
        ["enviar_aviso_penalidade()",          "Penalidade aplicada ao solicitante",   "SMTP / SendGrid"],
        ["enviar_comprovante_pagamento()",     "Multa paga com sucesso",               "SMTP / SendGrid"],
    ],
    [65, 70, 55]
)

pdf.subtitulo("12.2 PaymentService (app/external/payment_service.py)")
pdf.tabela(
    ["Metodo", "Comportamento atual (stub)", "Integracao sugerida"],
    [
        ["processar(valor, metodo)", "Sempre retorna status='aprovado'", "Stripe / MercadoPago / PagSeguro"],
    ],
    [55, 65, 70]
)

pdf.caixa_info(
    "Nota: A substituicao dos stubs por integracoes reais nao requer mudancas nas "
    "camadas de Negocio, Aplicacao ou Apresentacao, demonstrando o beneficio da "
    "Arquitetura em Camadas adotada."
)

# ══════════════════════════════════════════════════════════════════════════════
# 13. CONSIDERACOES FINAIS
# ══════════════════════════════════════════════════════════════════════════════
pdf.titulo("13. Consideracoes Finais")
pdf.corpo(
    "O sistema Joga Ai foi desenvolvido ao longo de 3 sprints seguindo o processo agil "
    "SCRUM, desde a especificacao de requisitos ate a implementacao completa com testes."
)
pdf.corpo(
    "A Arquitetura em Camadas adotada na Sprint 2 foi rigorosamente seguida na "
    "implementacao, resultando em um sistema modular, de facil manutencao e com "
    "baixo acoplamento entre os componentes."
)
pdf.corpo(
    "As 6 classes OOP do Diagrama de Classes (Sprint 2) foram implementadas fielmente, "
    "mantendo atributos, metodos, visibilidades e enumeracoes identicos ao diagrama UML, "
    "demonstrando a correspondencia direta entre modelagem e codigo."
)
pdf.corpo(
    "Os 66 testes automatizados cobrem todos os cenarios de uso definidos na Sprint 2, "
    "incluindo fluxos normais e alternativos, garantindo a corretude das regras de negocio "
    "e dos endpoints da API REST."
)

pdf.subtitulo("13.1 Possibilidades de Evolucao")
for item in [
    "Substituicao do SQLite por PostgreSQL (apenas uma linha de configuracao)",
    "Integracao real com servico de e-mail (SendGrid, SMTP)",
    "Integracao real com gateway de pagamento (Stripe, MercadoPago)",
    "Implementacao de websockets para chat em tempo real (substituir polling)",
    "Adicao de avaliacao de usuarios apos emprestimos (RF15)",
    "Historico completo de emprestimos por usuario (RF16)",
    "Suporte a imagens dos jogos (upload de foto da capa)",
]:
    pdf.bullet(item)

pdf.ln(6)
pdf.subtitulo("13.2 Equipe")
pdf.tabela(
    ["Integrante", "Matricula", "Responsabilidade Principal"],
    [
        ["Alvaro Lima Santos",           "2021067062", "Penalidades, notificacoes por e-mail, testes de validacao"],
        ["Beatriz Nogueira Alvares",     "2023001603", "Autenticacao, integracao BD, testes de integracao"],
        ["Lucas Dolabella de Castro Lopes","2023001549","Cadastro de jogos, busca, documentacao, Scrum Master"],
        ["Sarah Menks Sperber",          "2023001824", "Controle de prazos, integracao frontend/backend"],
        ["Vanessa Nascimento Silva",     "2023001816", "Sistema de emprestimos, chat, correcao de bugs"],
    ],
    [55, 26, 109]
)

pdf.output("Documentacao_JogaAi_Sprint3.pdf")
print("PDF gerado: Documentacao_JogaAi_Sprint3.pdf")