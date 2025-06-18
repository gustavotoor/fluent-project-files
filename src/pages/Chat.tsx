
import { useState, useEffect, useRef } from 'react';
import { useAuth } from '@/contexts/AuthContext';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Card } from '@/components/ui/card';
import { ScrollArea } from '@/components/ui/scroll-area';
import { Separator } from '@/components/ui/separator';
import Navbar from '@/components/Navbar';
import { Send, MessageCircle, Plus } from 'lucide-react';
import { useToast } from '@/hooks/use-toast';

interface Message {
  id: string;
  texto: string;
  remetente: 'user' | 'bot';
  data_envio: string;
}

interface ChatSession {
  id: string;
  created_at: string;
  preview: string;
}

const Chat = () => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [chatSessions, setChatSessions] = useState<ChatSession[]>([]);
  const [currentChatId, setCurrentChatId] = useState<string | null>(null);
  const [sidebarOpen, setSidebarOpen] = useState(true);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const { user } = useAuth();
  const { toast } = useToast();

  useEffect(() => {
    // Simulate loading chat sessions
    const demoSessions: ChatSession[] = [
      {
        id: '1',
        created_at: new Date().toISOString(),
        preview: 'Como criar um projeto...'
      },
      {
        id: '2',
        created_at: new Date(Date.now() - 86400000).toISOString(),
        preview: 'Upload de arquivos...'
      }
    ];
    setChatSessions(demoSessions);
    
    // Start with first session or create new one
    if (demoSessions.length > 0) {
      setCurrentChatId(demoSessions[0].id);
      loadChatMessages(demoSessions[0].id);
    }
  }, []);

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  const loadChatMessages = async (chatId: string) => {
    try {
      // Simulate API call
      const demoMessages: Message[] = [
        {
          id: '1',
          texto: 'Olá! Como posso ajudá-lo hoje?',
          remetente: 'bot',
          data_envio: new Date().toISOString()
        }
      ];
      setMessages(demoMessages);
    } catch (error) {
      console.error('Error loading messages:', error);
    }
  };

  const createNewChat = () => {
    const newChatId = Date.now().toString();
    const newSession: ChatSession = {
      id: newChatId,
      created_at: new Date().toISOString(),
      preview: 'Nova conversa'
    };
    
    setChatSessions([newSession, ...chatSessions]);
    setCurrentChatId(newChatId);
    setMessages([]);
  };

  const sendMessage = async () => {
    if (!inputValue.trim() || isLoading) return;

    const userMessage: Message = {
      id: Date.now().toString(),
      texto: inputValue,
      remetente: 'user',
      data_envio: new Date().toISOString()
    };

    setMessages(prev => [...prev, userMessage]);
    setInputValue('');
    setIsLoading(true);

    try {
      // Simulate typing delay
      await new Promise(resolve => setTimeout(resolve, 1000));

      const botResponse: Message = {
        id: (Date.now() + 1).toString(),
        texto: `SIMULAÇÃO: Recebi sua mensagem "${inputValue}". Como posso ajudar mais?`,
        remetente: 'bot',
        data_envio: new Date().toISOString()
      };

      setMessages(prev => [...prev, botResponse]);
      
      // Update session preview
      if (currentChatId) {
        setChatSessions(prev => 
          prev.map(session => 
            session.id === currentChatId 
              ? { ...session, preview: inputValue.substring(0, 20) + '...' }
              : session
          )
        );
      }
    } catch (error) {
      toast({
        title: "Erro",
        description: "Não foi possível enviar a mensagem",
        variant: "destructive",
      });
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900">
      <Navbar />
      <div className="flex h-[calc(100vh-4rem)]">
        {/* Sidebar */}
        <div className={`${sidebarOpen ? 'w-64' : 'w-0'} transition-all duration-300 bg-white dark:bg-gray-800 border-r border-gray-200 dark:border-gray-700 overflow-hidden`}>
          <div className="p-4">
            <Button 
              onClick={createNewChat}
              className="w-full mb-4"
              variant="outline"
            >
              <Plus className="mr-2 h-4 w-4" />
              Nova Conversa
            </Button>
            
            <ScrollArea className="h-[calc(100vh-10rem)]">
              <div className="space-y-2">
                {chatSessions.map((session) => (
                  <Card
                    key={session.id}
                    className={`p-3 cursor-pointer transition-colors hover:bg-gray-100 dark:hover:bg-gray-700 ${
                      currentChatId === session.id ? 'bg-blue-50 dark:bg-blue-900 border-blue-200 dark:border-blue-700' : ''
                    }`}
                    onClick={() => {
                      setCurrentChatId(session.id);
                      loadChatMessages(session.id);
                    }}
                  >
                    <div className="flex items-center space-x-2">
                      <MessageCircle className="h-4 w-4 text-gray-500" />
                      <div className="flex-1 min-w-0">
                        <p className="text-sm font-medium truncate">
                          {session.preview}
                        </p>
                        <p className="text-xs text-gray-500">
                          {new Date(session.created_at).toLocaleDateString()}
                        </p>
                      </div>
                    </div>
                  </Card>
                ))}
              </div>
            </ScrollArea>
          </div>
        </div>

        {/* Main Chat Area */}
        <div className="flex-1 flex flex-col">
          {/* Chat Messages */}
          <ScrollArea className="flex-1 p-4">
            <div className="max-w-3xl mx-auto space-y-4">
              {messages.length === 0 ? (
                <div className="text-center py-12">
                  <MessageCircle className="h-12 w-12 mx-auto text-gray-400 mb-4" />
                  <h3 className="text-lg font-medium text-gray-900 dark:text-gray-100 mb-2">
                    Bem-vindo ao ProjectManager Chat
                  </h3>
                  <p className="text-gray-500 dark:text-gray-400">
                    Comece uma conversa digitando sua mensagem abaixo
                  </p>
                </div>
              ) : (
                messages.map((message) => (
                  <div
                    key={message.id}
                    className={`flex ${message.remetente === 'user' ? 'justify-end' : 'justify-start'}`}
                  >
                    <div
                      className={`max-w-xs lg:max-w-md px-4 py-3 rounded-lg shadow-sm animate-fade-in ${
                        message.remetente === 'user'
                          ? 'chat-bubble-user text-white'
                          : 'chat-bubble-bot text-white'
                      }`}
                    >
                      <p className="text-sm whitespace-pre-wrap">{message.texto}</p>
                      <p className="text-xs opacity-75 mt-1">
                        {new Date(message.data_envio).toLocaleTimeString()}
                      </p>
                    </div>
                  </div>
                ))
              )}
              
              {isLoading && (
                <div className="flex justify-start">
                  <div className="bg-gray-200 dark:bg-gray-600 px-4 py-3 rounded-lg">
                    <div className="flex space-x-1">
                      <div className="w-2 h-2 bg-gray-500 rounded-full animate-pulse"></div>
                      <div className="w-2 h-2 bg-gray-500 rounded-full animate-pulse" style={{ animationDelay: '0.2s' }}></div>
                      <div className="w-2 h-2 bg-gray-500 rounded-full animate-pulse" style={{ animationDelay: '0.4s' }}></div>
                    </div>
                  </div>
                </div>
              )}
              
              <div ref={messagesEndRef} />
            </div>
          </ScrollArea>

          <Separator />

          {/* Message Input */}
          <div className="p-4 bg-white dark:bg-gray-800">
            <div className="max-w-3xl mx-auto">
              <div className="flex space-x-2">
                <Input
                  value={inputValue}
                  onChange={(e) => setInputValue(e.target.value)}
                  onKeyPress={handleKeyPress}
                  placeholder="Digite sua mensagem..."
                  className="flex-1"
                  disabled={isLoading}
                />
                <Button 
                  onClick={sendMessage}
                  disabled={!inputValue.trim() || isLoading}
                  size="sm"
                  className="px-4"
                >
                  <Send className="h-4 w-4" />
                </Button>
              </div>
            </div>
          </div>
        </div>

        {/* Sidebar Toggle for Mobile */}
        <Button
          variant="outline"
          size="sm"
          className="md:hidden fixed top-20 left-4 z-10"
          onClick={() => setSidebarOpen(!sidebarOpen)}
        >
          <MessageCircle className="h-4 w-4" />
        </Button>
      </div>
    </div>
  );
};

export default Chat;
