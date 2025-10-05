-- Inicialização do banco de dados para Imóvel Gestão
-- Este script será executado automaticamente quando o container PostgreSQL for criado

-- Configurações do banco de dados
SET timezone = 'America/Sao_Paulo';

-- Criar extensões úteis
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";

-- Log de inicialização
SELECT 'Banco de dados imovel_gestao inicializado com sucesso!' AS status;