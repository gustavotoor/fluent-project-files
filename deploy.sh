
#!/bin/bash

echo "🚀 Iniciando deploy do ProjectManager..."

# Verificar se o arquivo .env existe
if [ ! -f .env ]; then
    echo "❌ Arquivo .env não encontrado. Copiando de .env.example..."
    cp .env.example .env
    echo "⚠️  Configure as variáveis em .env antes de continuar!"
    exit 1
fi

# Verificar se as variáveis essenciais estão definidas
source .env
if [ -z "$DATABASE_URL" ] || [ -z "$JWT_SECRET" ]; then
    echo "❌ Variáveis DATABASE_URL e JWT_SECRET devem estar definidas no .env"
    exit 1
fi

echo "🔧 Verificando pré-requisitos..."

# Verificar se Docker está instalado
if ! command -v docker &> /dev/null; then
    echo "❌ Docker não encontrado. Instale o Docker primeiro."
    exit 1
fi

# Verificar se Docker Compose está instalado
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose não encontrado. Instale o Docker Compose primeiro."
    exit 1
fi

echo "📦 Parando containers existentes..."
docker-compose down --remove-orphans

echo "🧹 Limpando imagens antigas..."
docker system prune -f

echo "🏗️ Construindo imagens..."
docker-compose build --no-cache

echo "🚀 Iniciando containers..."
docker-compose up -d

echo "⏳ Aguardando containers iniciarem..."
sleep 15

echo "🔍 Verificando status dos containers..."
docker-compose ps

# Verificar se os containers estão rodando
FRONTEND_STATUS=$(docker-compose ps -q frontend | xargs docker inspect -f '{{.State.Status}}')
BACKEND_STATUS=$(docker-compose ps -q backend | xargs docker inspect -f '{{.State.Status}}')

if [ "$FRONTEND_STATUS" != "running" ] || [ "$BACKEND_STATUS" != "running" ]; then
    echo "❌ Erro: Um ou mais containers não estão rodando corretamente."
    echo "📝 Verificando logs..."
    docker-compose logs
    exit 1
fi

echo "✅ Health check dos serviços..."
sleep 10

# Testar frontend
if curl -f http://localhost:3000 > /dev/null 2>&1; then
    echo "✅ Frontend respondendo corretamente"
else
    echo "❌ Frontend não está respondendo"
    docker-compose logs frontend
fi

# Testar backend
if curl -f http://localhost:8000/health > /dev/null 2>&1; then
    echo "✅ Backend respondendo corretamente"
else
    echo "⚠️  Backend pode estar iniciando ou endpoint /health não implementado"
fi

echo ""
echo "🎉 Deploy concluído com sucesso!"
echo "📱 Frontend: http://localhost:3000"
echo "🔌 Backend: http://localhost:8000"
echo ""
echo "📊 Comandos úteis:"
echo "   Ver logs:        docker-compose logs -f"
echo "   Parar serviços:  docker-compose down"
echo "   Restart:         docker-compose restart"
echo "   Status:          docker-compose ps"
