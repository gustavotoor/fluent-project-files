
#!/bin/bash

echo "🚀 Instalando ProjectManager..."

# Parar containers existentes
echo "📦 Parando containers existentes..."
docker-compose down

# Remover imagens antigas (opcional)
echo "🧹 Limpando imagens antigas..."
docker-compose down --rmi all --volumes --remove-orphans 2>/dev/null || true

# Build e subir novos containers
echo "🏗️ Construindo e iniciando containers..."
docker-compose up --build -d

# Aguardar containers iniciarem
echo "⏳ Aguardando containers iniciarem..."
sleep 10

# Verificar status
echo "✅ Verificando status dos containers..."
docker-compose ps

# Mostrar logs se houver erro
if [ $? -ne 0 ]; then
    echo "❌ Erro ao iniciar containers. Verificando logs..."
    docker-compose logs
    exit 1
fi

echo "🎉 ProjectManager instalado com sucesso!"
echo "📱 Frontend: http://localhost:3000"
echo "🔌 Backend: http://localhost:8000"
echo ""
echo "📝 Para ver os logs:"
echo "   docker-compose logs -f"
echo ""
echo "🛑 Para parar:"
echo "   docker-compose down"
