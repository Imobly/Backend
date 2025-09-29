-- Inicialização do banco de dados para Imóvel Gestão
-- Este script será executado automaticamente quando o container MySQL for criado

-- Configurações do banco de dados
SET sql_mode = 'STRICT_TRANS_TABLES,NO_ZERO_DATE,NO_ZERO_IN_DATE,ERROR_FOR_DIVISION_BY_ZERO';
SET GLOBAL time_zone = '-03:00';

-- Criar usuário adicional para aplicação se necessário
-- (O usuário app_user já é criado via variáveis de ambiente)

-- Garantir que o charset está correto
ALTER DATABASE imovel_gestao CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- Log de inicialização
SELECT 'Banco de dados imovel_gestao inicializado com sucesso!' AS status;