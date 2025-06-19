
#!/bin/bash

echo "🔍 Verificação do Sistema ProjectManager"
echo "========================================"

# Verificar arquivos essenciais
echo "📁 Verificando arquivos essenciais..."
REQUIRED_FILES=(".env" "docker-compose.yml" "Dockerfile.frontend" "Dockerfile.backend" "nginx.conf")

for file in "${REQUIRED_FILES[@]}"; do
    if [ -f "$file" ]; then
        echo "✅ $file encontrado"
    else
        echo "❌ $file NÃO encontrado"
    fi
done

# Verificar estrutura de diretórios frontend
echo ""
echo "📂 Verificando estrutura frontend..."
FRONTEND_DIRS=("src" "src/components" "src/pages" "src/contexts")

for dir in "${FRONTEND_DIRS[@]}"; do
    if [ -d "$dir" ]; then
        echo "✅ Diretório $dir existe"
    else
        echo "❌ Diretório $dir NÃO existe"
    fi
done

# Verificar dependências
echo ""
echo "📦 Verificando dependências..."
if [ -f "package.json" ]; then
    echo "✅ package.json encontrado"
    
    # Verificar se node_modules existe
    if [ -d "node_modules" ]; then
        echo "✅ node_modules instalado"
    else
        echo "⚠️  node_modules não encontrado - execute 'npm install'"
    fi
else
    echo "❌ package.json NÃO encontrado"
fi

# Verificar configuração do banco
echo ""
echo "🗄️  Verificando configuração do banco..."
if [ -f ".env" ]; then
    source .env
    if [ -n "$DATABASE_URL" ]; then
        echo "✅ DATABASE_URL configurado"
    else
        echo "❌ DATABASE_URL não configurado"
    fi
    
    if [ -n "$JWT_SECRET" ]; then
        echo "✅ JWT_SECRET configurado"
    else
        echo "❌ JWT_SECRET não configurado"
    fi
else
    echo "❌ Arquivo .env não encontrado"
fi

# Verificar Docker
echo ""
echo "🐳 Verificando Docker..."
if command -v docker &> /dev/null; then
    echo "✅ Docker instalado"
    
    if command -v docker-compose &> /dev/null; then
        echo "✅ Docker Compose instalado"
    else
        echo "❌ Docker Compose NÃO instalado"
    fi
else
    echo "❌ Docker NÃO instalado"
fi

# Verificar portas
echo ""
echo "🔌 Verificando portas..."
if lsof -Pi :3000 -sTCP:LISTEN -t >/dev/null; then
    echo "⚠️  Porta 3000 já está em uso"
else
    echo "✅ Porta 3000 disponível"
fi

if lsof -Pi :8000 -sTCP:LISTEN -t >/dev/null; then
    echo "⚠️  Porta 8000 já está em uso"
else
    echo "✅ Porta 8000 disponível"
fi

echo ""
echo "📋 Verificação concluída!"
echo "Se houver erros acima, corrija-os antes do deploy."
