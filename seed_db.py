"""
Script para popular o banco de dados com jogos de tabuleiro de exemplo.
Cria jogos disponíveis e indisponíveis para demonstração.
"""

import os
import sys
from app import create_app
from app.database import db
from app.models.usuario import Usuario
from app.models.jogo import Jogo, StatusJogo

# Remove banco de dados existente se houver
if os.path.exists('jogaai.db'):
    os.remove('jogaai.db')
    print("Banco de dados anterior removido")

# Cria a aplicação e contexto
app = create_app()

with app.app_context():
    # Cria todas as tabelas
    db.create_all()
    print("Tabelas criadas")

    # Cria um usuário dono dos jogos
    joao = Usuario()
    joao.cadastrar(
        nome="João Silva",
        email="joao@gmail",
        senha="123"
    )
    db.session.add(joao)
    db.session.commit()
    print(f"Usuário criado: {joao.nome} (ID: {joao.id})")

    # Lista de jogos de tabuleiro para cadastrar
    jogos_dados = [
        {
            "nome": "Xadrez Clássico",
            "descricao": "O jogo de estratégia mais famoso do mundo. Perfeito para jogadores de todos os níveis.",
            "categoria": "Estratégia",
            "status": StatusJogo.DISPONIVEL.value
        },
        {
            "nome": "Damas",
            "descricao": "Jogo tradicional de estratégia e tática para 2 jogadores. Tabuleiro 8x8 com peças.",
            "categoria": "Estratégia",
            "status": StatusJogo.DISPONIVEL.value
        },
        {
            "nome": "Catan - Colonizadores",
            "descricao": "Jogo cooperativo onde você constrói assentamentos e cidades numa ilha. De 2-4 jogadores.",
            "categoria": "Cooperativo",
            "status": StatusJogo.DISPONIVEL.value
        },
        {
            "nome": "Carcassonne",
            "descricao": "Jogo de construção de mapa com peças de azulejo. Para 2-5 jogadores, partidas de 30-45 min.",
            "categoria": "Estratégia",
            "status": StatusJogo.EMPRESTADO.value
        },
        {
            "nome": "Ticket to Ride",
            "descricao": "Jogo de ferrovias onde você conecta cidades. Para 2-5 jogadores. Excelente para iniciantes.",
            "categoria": "Estratégia",
            "status": StatusJogo.DISPONIVEL.value
        },
        {
            "nome": "7 Wonders",
            "descricao": "Constrói civilizações antigas através de cartas. 2-7 jogadores. Partidas de ~45 minutos.",
            "categoria": "Estratégia",
            "status": StatusJogo.DISPONIVEL.value
        },
        {
            "nome": "Splendor",
            "descricao": "Jogo de mercador de joias. Colete gemas e construa um império. 2-4 jogadores.",
            "categoria": "Estratégia",
            "status": StatusJogo.EMPRESTADO.value
        },
        {
            "nome": "Pandemic",
            "descricao": "Jogo cooperativo onde sua equipe combate pandemias mundiais. 2-4 jogadores.",
            "categoria": "Cooperativo",
            "status": StatusJogo.DISPONIVEL.value
        },
        {
            "nome": "Codenames",
            "descricao": "Jogo de dedução e trabalho em equipe. 2-8+ jogadores. Muito dinâmico e divertido.",
            "categoria": "Dedução",
            "status": StatusJogo.DISPONIVEL.value
        },
        {
            "nome": "Dixit",
            "descricao": "Jogo criativo de narração e imaginação. 2-6 jogadores. Ótimo para reunir amigos.",
            "categoria": "Criatividade",
            "status": StatusJogo.EMPRESTADO.value
        },
        {
            "nome": "Azul",
            "descricao": "Jogo abstrato e elegante com mosaicos. 2-4 jogadores. Rápido e viciante!",
            "categoria": "Estratégia",
            "status": StatusJogo.DISPONIVEL.value
        },
        {
            "nome": "Everdell",
            "descricao": "Jogo de construção de árvore encantada com componentes lindos. 1-4 jogadores.",
            "categoria": "Estratégia",
            "status": StatusJogo.DISPONIVEL.value
        },
        {
            "nome": "Agricola",
            "descricao": "Jogo de gerenciamento de fazenda medieval. Muito estratégico. 1-5 jogadores.",
            "categoria": "Estratégia",
            "status": StatusJogo.EMPRESTADO.value
        },
        {
            "nome": "Banco Imobiliário",
            "descricao": "Clássico jogo de negociação imobiliária. Para toda a família. 2-8 jogadores.",
            "categoria": "Negociação",
            "status": StatusJogo.DISPONIVEL.value
        },
        {
            "nome": "War",
            "descricao": "Jogo de conquista e estratégia militar. Crie alianças e domine o mundo. 2-6 jogadores.",
            "categoria": "Estratégia",
            "status": StatusJogo.DISPONIVEL.value
        },
    ]

    # Cadastra todos os jogos
    for dados in jogos_dados:
        jogo = Jogo()
        jogo.dono_id = joao.id
        jogo.cadastrar(
            nome=dados["nome"],
            descricao=dados["descricao"],
            categoria=dados["categoria"]
        )
        jogo.status = dados["status"]
        db.session.add(jogo)

    db.session.commit()
    print(f"{len(jogos_dados)} jogos cadastrados no banco")

    # Conta estatísticas
    disponiveis = Jogo.query.filter_by(status=StatusJogo.DISPONIVEL.value).count()
    emprestados = Jogo.query.filter_by(status=StatusJogo.EMPRESTADO.value).count()

    print(f"\nEstatísticas do banco de dados:")
    print(f"   - Jogos disponíveis: {disponiveis}")
    print(f"   - Jogos emprestados: {emprestados}")
    print(f"   - Total de jogos: {disponiveis + emprestados}")
    print(f"\nBanco de dados 'jogaai.db' criado com sucesso!")
    print(f"   Use o arquivo para demonstrações e testes.")
