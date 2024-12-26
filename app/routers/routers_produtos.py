from typing import Dict, List
from fastapi import APIRouter, HTTPException
from app.models.models_produtos import (
    CriarProduto,
    HistoricoCompras,
    Preferencias,
    Produto,
)
from .routers_usuarios import usuarios

router = APIRouter()

produtos: List[Produto] = []
contador_produto: int = 1

historico_de_compras: Dict[int, List[int]] = {}


@router.post("/produtos/", response_model=Produto)
def criar_produto(produto: CriarProduto) -> Produto:
    """
    Cria um novo Produto.

    args:
        produto (CriarProduto): Objeto contendo os dados dos produtos a serem criados.

    returns:
        Produto: Objeto do tipo Produto criado com um ID gerado.
    """

    global contador_produto
    novo_produto = Produto(id=contador_produto, **produto.model_dump())
    produtos.append(novo_produto)
    contador_produto += 1
    return novo_produto


# Rota para listar todos os produtos


@router.get("/produtos/", response_model=List[Produto])
def listar_produtos() -> List[Produto]:
    """
    Lista todos os produtos cadastrados.

    returns:
        List[Produto]: Lista de objetos do tipo Produto.
    """
    return produtos


# Rota para simular a criação do histórico de compras de um usuário


@router.post("/historico_compras/{usuario_id}")
def adicionar_historico_compras(
    usuario_id: int, compras: HistoricoCompras
) -> Dict[str, str]:
    """
    Adiciona ou atualiza um histórico de compras de um usuário.

    args:
        usuario_id (int): ID do usuário.
        compras (HistoricoCompras): Objeto contendo os IDs dos produtos comprados.

    returns:
        Dict[str, str]: Mensagem de sucesso.
    """
    if usuario_id not in [usuario.id for usuario in usuarios]:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    historico_de_compras[usuario_id] = compras.produtos_ids
    return {"mensagem": "Histórico de compras atualizado"}


# Rota para recomendações de produtos


@router.post("/recomendacoes/{usuario_id}", response_model=List[Produto])
def recomendar_produtos(usuario_id: int, preferencias: Preferencias) -> List[Produto]:
    """
    Recomenda produtos com base no histórico de compras e nas preferências do usuário.

    args:
        usuario_id (int): ID do usuário para o qual as recomendações serão feitas.
        preferencias (Preferencias): Objeto contendo as preferências do usuário.

    Raises:
        HTTPException: Caso o histórico de compras do usuário não seja encontrado.

    returns:
        List[Produto]: Lista de objetos do tipo Produto recomendados.
    """

    if usuario_id not in historico_de_compras:
        raise HTTPException(
            status_code=404, detail="Histórico de compras não encontrado"
        )

    produtos_recomendados = []

    # Buscar produtos com base no histórico de compras do usuário

    produtos_recomendados = [
        produto
        for produto_id in historico_de_compras[usuario_id]
        for produto in produtos
        if produto.id == produto_id
    ]

    # Filtrar as recomendações com base nas preferências
    produtos_recomendados_categoria = [
        p for p in produtos_recomendados if p.categoria in preferencias.categorias
    ]  # Preferencias de categorias
    
    produtos_recomendados_filtrados = []
    for produto in produtos_recomendados_categoria:
        for tag in produto.tags:
            if tag in preferencias.tags:
                produtos_recomendados_filtrados.append(produto)
                break

    return produtos_recomendados_filtrados
