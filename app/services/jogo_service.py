from app.database import db
from app.models.jogo import Jogo, StatusJogo


class JogoService:

    @staticmethod
    def cadastrar(nome: str, descricao: str, categoria: str, dono_id: str) -> Jogo:
        jogo = Jogo()
        jogo.cadastrar(nome, descricao, categoria)
        jogo.dono_id = dono_id
        db.session.add(jogo)
        db.session.commit()
        return jogo

    @staticmethod
    def listar_disponiveis(busca: str = None) -> list:
        query = Jogo.query.filter_by(status=StatusJogo.DISPONIVEL.value)
        if busca:
            query = query.filter(
                (Jogo.nome.ilike(f"%{busca}%")) | (Jogo.categoria.ilike(f"%{busca}%"))
            )
        return query.all()

    @staticmethod
    def listar_todos(busca: str = None) -> list:
        query = Jogo.query
        if busca:
            query = query.filter(
                (Jogo.nome.ilike(f"%{busca}%")) | (Jogo.categoria.ilike(f"%{busca}%"))
            )
        return query.all()

    @staticmethod
    def listar_por_usuario(usuario_id: str) -> list:
        return Jogo.query.filter_by(dono_id=usuario_id).all()

    @staticmethod
    def obter(jogo_id: str) -> Jogo:
        jogo = Jogo.query.get(jogo_id)
        if not jogo:
            raise ValueError("Jogo não encontrado.")
        return jogo

    @staticmethod
    def atualizar(jogo_id: str, usuario_id: str, dados: dict) -> Jogo:
        jogo = JogoService.obter(jogo_id)
        if jogo.dono_id != usuario_id:
            raise PermissionError("Você não tem permissão para editar este jogo.")
        jogo.atualizar(dados)
        db.session.commit()
        return jogo

    @staticmethod
    def remover(jogo_id: str, usuario_id: str) -> None:
        jogo = JogoService.obter(jogo_id)
        if jogo.dono_id != usuario_id:
            raise PermissionError("Você não tem permissão para remover este jogo.")
        if jogo.status == "EMPRESTADO":
            raise ValueError("Não é possível remover um jogo que está emprestado.")
        db.session.delete(jogo)
        db.session.commit()