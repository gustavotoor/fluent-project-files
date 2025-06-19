
# Guia de Solução de Problemas - ProjectManager

## Problemas Comuns de Deploy

### 1. Containers não iniciam

**Sintomas:**
- `docker-compose up` falha
- Containers param imediatamente

**Soluções:**
```bash
# Verificar logs
docker-compose logs

# Verificar arquivo .env
cat .env

# Rebuildar sem cache
docker-compose build --no-cache
```

### 2. Frontend não carrega

**Sintomas:**
- Página em branco
- Erro 502/503

**Soluções:**
```bash
# Verificar status do nginx
docker-compose exec frontend nginx -t

# Verificar logs do frontend
docker-compose logs frontend

# Verificar se os arquivos foram copiados
docker-compose exec frontend ls -la /usr/share/nginx/html
```

### 3. Backend não responde

**Sintomas:**
- API retorna 500/502
- Timeout nas requisições

**Soluções:**
```bash
# Verificar logs do backend
docker-compose logs backend

# Testar conexão com banco
docker-compose exec backend python -c "import os; print(os.getenv('DATABASE_URL'))"

# Verificar se uvicorn está rodando
docker-compose exec backend ps aux | grep uvicorn
```

### 4. Problemas de CORS

**Sintomas:**
- Erro de CORS no browser
- Requisições bloqueadas

**Soluções:**
- Verificar variável `ALLOWED_ORIGINS` no .env
- Configurar nginx proxy corretamente
- Verificar headers de CORS no backend

### 5. Upload de arquivos falha

**Sintomas:**
- Erro ao fazer upload
- Arquivos não são salvos

**Soluções:**
```bash
# Verificar permissões do diretório
docker-compose exec backend ls -la /app/uploads

# Verificar espaço em disco
docker system df

# Verificar limite de tamanho
grep MAX_FILE_SIZE .env
```

## Comandos Úteis

### Logs e Debug
```bash
# Ver todos os logs
docker-compose logs

# Ver logs em tempo real
docker-compose logs -f

# Ver logs de um serviço específico
docker-compose logs backend

# Ver últimas 50 linhas
docker-compose logs --tail=50
```

### Gerenciamento de Containers
```bash
# Parar todos os serviços
docker-compose down

# Restart de um serviço
docker-compose restart backend

# Rebuild de um serviço
docker-compose up --build backend

# Verificar status
docker-compose ps
```

### Limpeza
```bash
# Limpar containers parados
docker container prune

# Limpar imagens não utilizadas
docker image prune

# Limpeza completa
docker system prune -a
```

## Verificações de Saúde

### Frontend
```bash
curl -I http://localhost:3000
```

### Backend
```bash
curl -I http://localhost:8000/health
```

### Banco de Dados
```bash
# Testar conexão (substitua com suas credenciais)
docker-compose exec backend python -c "
import asyncpg
import asyncio
async def test():
    conn = await asyncpg.connect('$DATABASE_URL')
    await conn.close()
    print('Conexão OK')
asyncio.run(test())
"
```

## Configuração de Produção

### Variáveis Obrigatórias
- `DATABASE_URL`: String de conexão do PostgreSQL
- `JWT_SECRET`: Chave secreta para JWT (mínimo 256 bits)
- `ALLOWED_ORIGINS`: Domínios permitidos para CORS

### Recomendações de Segurança
1. Use HTTPS em produção
2. Configure firewall adequadamente
3. Use secrets management para credenciais
4. Configure backup automático do banco
5. Monitor logs e métricas

### Performance
1. Configure cache no nginx
2. Use CDN para assets estáticos
3. Configure compressão gzip
4. Monitor uso de recursos

## Contato de Suporte

Em caso de problemas persistentes:
1. Colete logs completos
2. Documente passos para reproduzir
3. Verifique configurações de ambiente
