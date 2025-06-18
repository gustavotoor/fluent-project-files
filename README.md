
# ProjectManager 🚀

Sistema completo de gestão de projetos com upload de arquivos, chat inteligente e autenticação JWT.

## ✨ Funcionalidades

- **Autenticação JWT** - Login/registro seguro com proteção de rotas
- **Chat Inteligente** - Sistema de chat estilo ChatGPT com histórico
- **Gestão de Projetos** - Criação e acompanhamento de projetos
- **Upload de Arquivos** - Upload vinculado a projetos com tipos permitidos
- **Interface Responsiva** - Design moderno que funciona em mobile, tablet e desktop
- **Tema Claro/Escuro** - Alternância entre temas com preferência salva

## 🛠️ Tecnologias

### Frontend
- **React 18** + TypeScript
- **Vite** para build otimizado
- **Tailwind CSS** para estilização
- **shadcn/ui** para componentes
- **React Router** para navegação
- **Context API** para gerenciamento de estado

### Backend (Estrutura proposta)
- **FastAPI** + SQLAlchemy
- **PostgreSQL** (banco existente)
- **JWT** para autenticação
- **Alembic** para migrations
- **Pydantic** para validação

## 🚀 Modo de Simulação

A aplicação possui dois modos de operação:

### CHAT_SIMULATION=true (Padrão)
- Respostas simuladas do chat
- Funciona sem backend
- Ideal para desenvolvimento e demonstrações

### CHAT_SIMULATION=false
- Integração com webhook n8n
- Endpoint: `http://localhost:5678/webhook/envia-mensagem`
- Payload: `{chat_id, user_id, data_envio, mensagem}`
- Retorna: `{resposta: "texto da resposta"}`

## 📱 Design Responsivo

A aplicação é totalmente responsiva e funciona perfeitamente em:
- 📱 **Mobile** (320px+)
- 📱 **Tablet** (768px+)
- 💻 **Desktop** (1024px+)

## 🎨 Interface

- **Cores primárias**: Azul (#3B82F6) com gradientes
- **Tema claro/escuro** com transições suaves
- **Animações sutis** para melhor UX
- **Micro-interações** em botões e cards
- **Layout sidebar** colapsível no chat

## 🔒 Autenticação

- JWT armazenado em localStorage
- Context API para gerenciamento de estado de auth
- ProtectedRoute para rotas privadas
- Redirects automáticos baseados no status de auth

## 📁 Estrutura de Arquivos Permitidos

- **Documentos**: PDF, DOC, DOCX
- **Planilhas**: XLS, XLSX
- **Imagens**: JPG, JPEG
- **Texto**: TXT
- **Limite**: 10MB por arquivo

## 🐳 Deploy com Docker

### Variáveis de Ambiente (.env)
```bash
# Database
DATABASE_URL=postgresql://user:password@host:5432/dbname

# JWT
JWT_SECRET=your-super-secret-key

# Chat Mode
CHAT_SIMULATION=true

# Upload
UPLOAD_FOLDER=/app/uploads
```

### Docker Compose
```bash
# Build e subir aplicação
docker-compose up --build -d

# Logs
docker-compose logs -f

# Parar
docker-compose down
```

### Script de Instalação
```bash
chmod +x install.sh
./install.sh
```

## 📊 Banco de Dados

### Tabelas Principais

#### usuarios
- id (UUID, PK)
- nome (VARCHAR)
- email (VARCHAR, UNIQUE)
- senha_hash (VARCHAR)
- created_at (TIMESTAMP)

#### projetos
- id (UUID, PK)
- nome (VARCHAR)
- data_solicitacao (DATE)
- prazo_entrega (DATE)
- user_id (UUID, FK)

#### chats
- id (UUID, PK)
- user_id (UUID, FK)
- created_at (TIMESTAMP)

#### mensagens
- id (UUID, PK)
- chat_id (UUID, FK)
- texto (TEXT)
- remetente (ENUM: user/bot)
- data_envio (TIMESTAMP)

#### arquivos
- id (UUID, PK)
- nome_arquivo (VARCHAR)
- tipo (VARCHAR)
- caminho (VARCHAR)
- projeto_id (UUID, FK)
- user_id (UUID, FK)
- data_upload (TIMESTAMP)

## 🔌 API Endpoints (Backend)

### Autenticação
- `POST /auth/register` - Criar usuário
- `POST /auth/login` - Login e obter JWT

### Chat
- `GET /chat/sessoes` - Listar chats do usuário
- `GET /chat/{chat_id}` - Mensagens da sessão
- `POST /chat/mensagem` - Enviar mensagem

### Projetos
- `GET /projetos/distintos` - Projetos únicos
- `POST /projetos/` - Criar projeto

### Upload
- `POST /upload/` - Upload de arquivo

## 🔧 Desenvolvimento

### Instalação Local
```bash
# Clone o repositório
git clone <repo-url>
cd projectmanager

# Instale dependências
npm install

# Inicie o desenvolvimento
npm run dev
```

### Comandos Úteis
```bash
# Build para produção
npm run build

# Preview do build
npm run preview

# Lint
npm run lint
```

## 🌟 Funcionalidades Destacadas

1. **Chat com Histórico** - Sidebar com conversas anteriores
2. **Upload Drag & Drop** - Interface intuitiva para upload
3. **Status de Projetos** - Badges coloridos indicando urgência
4. **Responsividade Total** - Layout que se adapta a qualquer tela
5. **Tema Persistente** - Preferência de tema salva no localStorage
6. **Feedback Visual** - Toasts para todas as ações importantes

## 📝 TODO / Melhorias Futuras

- [ ] Implementação do backend FastAPI
- [ ] Migrations do banco de dados
- [ ] Autenticação social (Google, GitHub)
- [ ] Notificações push
- [ ] Filtros avançados de projetos
- [ ] Exportação de dados
- [ ] API de relatórios
- [ ] Integração com calendário

## 🤝 Contribuição

1. Fork o projeto
2. Crie sua feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

---

**ProjectManager** - Transformando a gestão de projetos com tecnologia moderna! 🚀
