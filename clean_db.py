"""
Script para limpar o banco de dados, removendo todas as tabelas e dados.
Use com cuidado - esta ação é irreversível!
"""

import os
import sys
import shutil
from pathlib import Path

def limpar_bd():
    """
    Limpar usando SQLAlchemy (drops todas as tabelas).
    Use esta função se quiser manter a pasta instance.
    """
    
    print("=" * 70)
    print("LIMPEZA DE TABELAS (SQLAlchemy) - JOGA AÍ")
    print("=" * 70)
    print()
    
    try:
        from app import create_app
        from app.database import db
        
        # Criar app e contexto
        app = create_app()
        
        with app.app_context():
            # Obter todas as tabelas
            inspector = db.inspect(db.engine)
            tabelas = inspector.get_table_names()
            
            if not tabelas:
                print("Nenhuma tabela encontrada. Banco de dados já está limpo!")
                print()
                return
            
            # Exibir tabelas a serem removidas
            print("Tabelas encontradas:")
            print()
            for tabela in tabelas:
                print(f"   - {tabela}")
            print()
            
            # Confirmação
            print("ATENÇÃO: Esta ação é IRREVERSÍVEL!")
            print("   Todas as tabelas serão removidas.")
            print()
            resposta = input("Deseja continuar? (sim/não): ").strip().lower()
            print()
            
            if resposta not in ['sim', 's', 'yes', 'y']:
                print("Operação cancelada.")
                print()
                return
            
            # Remover todas as tabelas
            db.drop_all()
            
            print("Todas as tabelas foram removidas com sucesso!")
            print()
            print("Para recriar as tabelas com dados de exemplo, execute:")
            print("   python seed_db.py")
            print()
    
    except Exception as e:
        print(f"Erro ao limpar banco de dados: {str(e)}")
        print()
        import traceback
        traceback.print_exc()
        print()


if __name__ == "__main__":
    limpar_bd()
