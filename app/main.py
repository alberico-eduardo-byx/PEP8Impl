from typing import Dict
from fastapi import FastAPI
from .routers import routers_usuarios, routers_produtos

MENSAGEM_HOME: str = "Bem-vindo à API de Recomendação de Produtos"

app = FastAPI()
app.include_router(routers_produtos.router)
app.include_router(routers_usuarios.router)


@app.get("/")
def home() -> Dict[str, str]:
    global MENSAGEM_HOME
    return {"mensagem": MENSAGEM_HOME}
