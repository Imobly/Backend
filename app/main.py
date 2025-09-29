from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os
from app.core.config import settings
from app.db.session import create_tables
from app.api.v1.api import api_router

# Inicializar aplicação FastAPI
app = FastAPI(
    title="Imóvel Gestão API",
    description="API para gestão de propriedades imobiliárias",
    version="1.0.0",
    openapi_url="/api/v1/openapi.json",
    docs_url="/api/v1/docs",
    redoc_url="/api/v1/redoc"
)

# Configuração CORS para comunicação com frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],
    allow_headers=["*"],
)

# Criar diretório de uploads se não existir
os.makedirs(settings.UPLOAD_DIR, exist_ok=True)

# Servir arquivos estáticos (uploads)
app.mount("/uploads", StaticFiles(directory=settings.UPLOAD_DIR), name="uploads")

# Incluir rotas da API
app.include_router(api_router, prefix="/api/v1")

@app.on_event("startup")
async def startup_event():
    """Executar na inicialização da aplicação"""
    # Criar tabelas no banco de dados
    create_tables()

@app.get("/")
async def root():
    """Endpoint raiz"""
    return {
        "message": "Imóvel Gestão API",
        "version": "1.0.0",
        "docs": "/api/v1/docs"
    }

@app.get("/health")
async def health_check():
    """Verificação de saúde da aplicação"""
    return {"status": "healthy"}

@app.get("/")
def read_root():
    return {
        "message": f"Bem-vindo ao {settings.PROJECT_NAME}",
        "version": settings.VERSION,
        "docs": "/docs",
        "api": settings.API_V1_STR
    }

@app.get("/health")
def health_check():
    return {"status": "healthy", "service": settings.PROJECT_NAME}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app, 
        host=settings.HOST, 
        port=settings.PORT,
        reload=settings.DEBUG
    )