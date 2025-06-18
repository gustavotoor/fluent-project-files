
# Database Schema - ProjectManager

## Visão Geral

O banco de dados do ProjectManager é projetado para suportar autenticação de usuários, gestão de projetos, sistema de chat e upload de arquivos.

## Diagrama de Relacionamentos

```
┌─────────────────┐       ┌─────────────────┐
│    usuarios     │       │    projetos     │
├─────────────────┤       ├─────────────────┤
│ id (UUID, PK)   │       │ id (UUID, PK)   │
│ nome            │◄──────┤ user_id (FK)    │
│ email (UNIQUE)  │       │ nome            │
│ senha_hash      │       │ data_solicitacao│
│ created_at      │       │ prazo_entrega   │
└─────────────────┘       └─────────────────┘
          │                         │
          │                         │
          │               ┌─────────────────┐
          │               │    arquivos     │
          │               ├─────────────────┤
          │               │ id (UUID, PK)   │
          │               │ nome_arquivo    │
          │               │ tipo            │
          │               │ caminho         │
          │               │ projeto_id (FK) │◄─────┘
          │               │ user_id (FK)    │◄─────┐
          │               │ data_upload     │      │
          │               └─────────────────┘      │
          │                                        │
          │               ┌─────────────────┐      │
          └───────────────┤     chats       │      │
                          ├─────────────────┤      │
                          │ id (UUID, PK)   │      │
                          │ user_id (FK)    │──────┘
                          │ created_at      │
                          └─────────────────┘
                                    │
                                    │
                          ┌─────────────────┐
                          │   mensagens     │
                          ├─────────────────┤
                          │ id (UUID, PK)   │
                          │ chat_id (FK)    │◄─────┘
                          │ texto           │
                          │ remetente       │
                          │ data_envio      │
                          └─────────────────┘
```

## Definições das Tabelas

### 1. Tabela: usuarios

Armazena informações dos usuários do sistema.

```sql
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

CREATE TABLE usuarios (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    nome VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    senha_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Índices
CREATE INDEX idx_usuarios_email ON usuarios(email);
CREATE INDEX idx_usuarios_created_at ON usuarios(created_at);
```

### 2. Tabela: projetos

Armazena informações dos projetos criados pelos usuários.

```sql
CREATE TABLE projetos (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    nome VARCHAR(255) NOT NULL,
    data_solicitacao DATE NOT NULL,
    prazo_entrega DATE NOT NULL,
    user_id UUID NOT NULL REFERENCES usuarios(id) ON DELETE CASCADE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Índices
CREATE INDEX idx_projetos_user_id ON projetos(user_id);
CREATE INDEX idx_projetos_prazo_entrega ON projetos(prazo_entrega);
CREATE INDEX idx_projetos_created_at ON projetos(created_at);
```

### 3. Tabela: chats

Armazena as sessões de chat dos usuários.

```sql
CREATE TABLE chats (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES usuarios(id) ON DELETE CASCADE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Índices
CREATE INDEX idx_chats_user_id ON chats(user_id);
CREATE INDEX idx_chats_created_at ON chats(created_at);
```

### 4. Tabela: mensagens

Armazena as mensagens trocadas nos chats.

```sql
CREATE TYPE remetente_enum AS ENUM ('user', 'bot');

CREATE TABLE mensagens (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    chat_id UUID NOT NULL REFERENCES chats(id) ON DELETE CASCADE,
    texto TEXT NOT NULL,
    remetente remetente_enum NOT NULL,
    data_envio TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Índices
CREATE INDEX idx_mensagens_chat_id ON mensagens(chat_id);
CREATE INDEX idx_mensagens_data_envio ON mensagens(data_envio);
CREATE INDEX idx_mensagens_remetente ON mensagens(remetente);
```

### 5. Tabela: arquivos

Armazena informações dos arquivos enviados pelos usuários.

```sql
CREATE TABLE arquivos (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    nome_arquivo VARCHAR(255) NOT NULL,
    tipo VARCHAR(100) NOT NULL,
    caminho VARCHAR(500) NOT NULL,
    projeto_id UUID NOT NULL REFERENCES projetos(id) ON DELETE CASCADE,
    user_id UUID NOT NULL REFERENCES usuarios(id) ON DELETE CASCADE,
    data_upload TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Índices
CREATE INDEX idx_arquivos_projeto_id ON arquivos(projeto_id);
CREATE INDEX idx_arquivos_user_id ON arquivos(user_id);
CREATE INDEX idx_arquivos_data_upload ON arquivos(data_upload);
CREATE INDEX idx_arquivos_tipo ON arquivos(tipo);
```

## Scripts de Migração

### Migration 001: Criar estrutura inicial

```sql
-- 001_initial_schema.sql

-- Habilitar extensão para UUID
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- Criar enum para remetente
CREATE TYPE remetente_enum AS ENUM ('user', 'bot');

-- Criar tabela usuarios
CREATE TABLE usuarios (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    nome VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    senha_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Criar tabela projetos
CREATE TABLE projetos (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    nome VARCHAR(255) NOT NULL,
    data_solicitacao DATE NOT NULL,
    prazo_entrega DATE NOT NULL,
    user_id UUID NOT NULL REFERENCES usuarios(id) ON DELETE CASCADE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Criar tabela chats
CREATE TABLE chats (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES usuarios(id) ON DELETE CASCADE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Criar tabela mensagens
CREATE TABLE mensagens (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    chat_id UUID NOT NULL REFERENCES chats(id) ON DELETE CASCADE,
    texto TEXT NOT NULL,
    remetente remetente_enum NOT NULL,
    data_envio TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Criar tabela arquivos
CREATE TABLE arquivos (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    nome_arquivo VARCHAR(255) NOT NULL,
    tipo VARCHAR(100) NOT NULL,
    caminho VARCHAR(500) NOT NULL,
    projeto_id UUID NOT NULL REFERENCES projetos(id) ON DELETE CASCADE,
    user_id UUID NOT NULL REFERENCES usuarios(id) ON DELETE CASCADE,
    data_upload TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
```

### Migration 002: Criar índices

```sql
-- 002_create_indexes.sql

-- Índices para usuarios
CREATE INDEX idx_usuarios_email ON usuarios(email);
CREATE INDEX idx_usuarios_created_at ON usuarios(created_at);

-- Índices para projetos
CREATE INDEX idx_projetos_user_id ON projetos(user_id);
CREATE INDEX idx_projetos_prazo_entrega ON projetos(prazo_entrega);
CREATE INDEX idx_projetos_created_at ON projetos(created_at);

-- Índices para chats
CREATE INDEX idx_chats_user_id ON chats(user_id);
CREATE INDEX idx_chats_created_at ON chats(created_at);

-- Índices para mensagens
CREATE INDEX idx_mensagens_chat_id ON mensagens(chat_id);
CREATE INDEX idx_mensagens_data_envio ON mensagens(data_envio);
CREATE INDEX idx_mensagens_remetente ON mensagens(remetente);

-- Índices para arquivos
CREATE INDEX idx_arquivos_projeto_id ON arquivos(projeto_id);
CREATE INDEX idx_arquivos_user_id ON arquivos(user_id);
CREATE INDEX idx_arquivos_data_upload ON arquivos(data_upload);
CREATE INDEX idx_arquivos_tipo ON arquivos(tipo);
```

## Dados de Exemplo

### Usuário Administrador

```sql
-- Criar usuário admin (senha: admin123)
INSERT INTO usuarios (nome, email, senha_hash) VALUES (
    'Administrador',
    'admin@projectmanager.com',
    '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewGGLJhYLhGGaGp.' -- admin123
);

-- Obter ID do usuário admin para usar nas próximas inserções
-- SELECT id FROM usuarios WHERE email = 'admin@projectmanager.com';
```

### Projetos de Exemplo

```sql
-- Inserir projetos de exemplo (substitua USER_ID_AQUI pelo ID real do usuário)
INSERT INTO projetos (nome, data_solicitacao, prazo_entrega, user_id) VALUES 
(
    'Website Corporativo',
    '2024-01-15',
    '2024-02-15',
    'USER_ID_AQUI'
),
(
    'Sistema de Vendas',
    '2024-01-20',
    '2024-03-01',
    'USER_ID_AQUI'
),
(
    'App Mobile',
    '2024-02-01',
    '2024-03-15',
    'USER_ID_AQUI'
);
```

### Chat de Exemplo

```sql
-- Criar chat de exemplo
INSERT INTO chats (user_id) VALUES ('USER_ID_AQUI');

-- Inserir mensagens de exemplo (substitua CHAT_ID_AQUI pelo ID do chat criado)
INSERT INTO mensagens (chat_id, texto, remetente) VALUES 
(
    'CHAT_ID_AQUI',
    'Olá! Como posso ajudá-lo hoje?',
    'bot'
),
(
    'CHAT_ID_AQUI',
    'Preciso de ajuda com meu projeto',
    'user'
),
(
    'CHAT_ID_AQUI',
    'Claro! Posso ajudá-lo com informações sobre seus projetos. Que tipo de ajuda você precisa?',
    'bot'
);
```

## Queries Úteis

### Listar projetos com status baseado no prazo

```sql
SELECT 
    p.id,
    p.nome,
    p.data_solicitacao,
    p.prazo_entrega,
    u.nome as usuario,
    CASE 
        WHEN p.prazo_entrega < CURRENT_DATE THEN 'Atrasado'
        WHEN p.prazo_entrega <= CURRENT_DATE + INTERVAL '7 days' THEN 'Urgente'
        ELSE 'No prazo'
    END as status
FROM projetos p
JOIN usuarios u ON p.user_id = u.id
ORDER BY p.prazo_entrega ASC;
```

### Obter estatísticas de uploads por usuário

```sql
SELECT 
    u.nome,
    COUNT(a.id) as total_arquivos,
    COUNT(DISTINCT a.projeto_id) as projetos_com_arquivos,
    STRING_AGG(DISTINCT a.tipo, ', ') as tipos_arquivo
FROM usuarios u
LEFT JOIN arquivos a ON u.id = a.user_id
GROUP BY u.id, u.nome
ORDER BY total_arquivos DESC;
```

### Listar mensagens recentes de um chat

```sql
SELECT 
    m.texto,
    m.remetente,
    m.data_envio,
    u.nome as usuario
FROM mensagens m
JOIN chats c ON m.chat_id = c.id
JOIN usuarios u ON c.user_id = u.id
WHERE c.id = 'CHAT_ID_AQUI'
ORDER BY m.data_envio ASC;
```

## Backup e Restauração

### Backup

```bash
# Backup completo
pg_dump -h hostname -U username -d projectmanager > backup_$(date +%Y%m%d_%H%M%S).sql

# Backup apenas estrutura
pg_dump -h hostname -U username -d projectmanager --schema-only > schema_backup.sql

# Backup apenas dados
pg_dump -h hostname -U username -d projectmanager --data-only > data_backup.sql
```

### Restauração

```bash
# Restaurar backup completo
psql -h hostname -U username -d projectmanager < backup_file.sql
```

## Considerações de Performance

1. **Índices**: Todos os campos frequentemente consultados possuem índices
2. **Particionamento**: Para grandes volumes, considere particionar `mensagens` por data
3. **Arquivamento**: Implemente rotina para arquivar mensagens antigas
4. **Backup**: Configure backups automáticos regulares
5. **Monitoramento**: Use pg_stat_statements para monitorar queries lentas

## Segurança

1. **Senhas**: Sempre usar bcrypt para hash de senhas (custo 12+)
2. **SQL Injection**: Usar sempre prepared statements/parametrized queries
3. **RBAC**: Implementar controle de acesso baseado em roles se necessário
4. **Auditoria**: Considere adicionar campos de auditoria (created_by, updated_by, etc.)
5. **Soft Delete**: Para dados críticos, implemente soft delete ao invés de DELETE físico
