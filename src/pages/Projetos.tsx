
import { useState, useEffect } from 'react';
import { useAuth } from '@/contexts/AuthContext';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Dialog, DialogContent, DialogDescription, DialogHeader, DialogTitle, DialogTrigger } from '@/components/ui/dialog';
import { Badge } from '@/components/ui/badge';
import Navbar from '@/components/Navbar';
import { Plus, Calendar, Clock, User } from 'lucide-react';
import { useToast } from '@/hooks/use-toast';

interface Projeto {
  id: string;
  nome: string;
  data_solicitacao: string;
  prazo_entrega: string;
  user_id: string;
}

const Projetos = () => {
  const [projetos, setProjetos] = useState<Projeto[]>([]);
  const [nome, setNome] = useState('');
  const [dataSolicitacao, setDataSolicitacao] = useState('');
  const [prazoEntrega, setPrazoEntrega] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [dialogOpen, setDialogOpen] = useState(false);
  const { user } = useAuth();
  const { toast } = useToast();

  useEffect(() => {
    loadProjetos();
  }, []);

  const loadProjetos = async () => {
    try {
      // Simulate API call
      const demoProjetos: Projeto[] = [
        {
          id: '1',
          nome: 'Website Corporativo',
          data_solicitacao: '2024-01-15',
          prazo_entrega: '2024-02-15',
          user_id: user?.id || '1'
        },
        {
          id: '2',
          nome: 'Sistema de Vendas',
          data_solicitacao: '2024-01-20',
          prazo_entrega: '2024-03-01',
          user_id: user?.id || '1'
        }
      ];
      setProjetos(demoProjetos);
    } catch (error) {
      console.error('Error loading projects:', error);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);

    try {
      const novoProjeto: Projeto = {
        id: Date.now().toString(),
        nome,
        data_solicitacao: dataSolicitacao,
        prazo_entrega: prazoEntrega,
        user_id: user?.id || '1'
      };

      setProjetos(prev => [novoProjeto, ...prev]);
      
      // Clear form
      setNome('');
      setDataSolicitacao('');
      setPrazoEntrega('');
      setDialogOpen(false);
      
      toast({
        title: "Projeto criado com sucesso!",
        description: `O projeto "${nome}" foi adicionado.`,
      });
    } catch (error) {
      toast({
        title: "Erro",
        description: "Não foi possível criar o projeto",
        variant: "destructive",
      });
    } finally {
      setIsLoading(false);
    }
  };

  const getStatusBadge = (prazoEntrega: string) => {
    const hoje = new Date();
    const prazo = new Date(prazoEntrega);
    const diffDays = Math.ceil((prazo.getTime() - hoje.getTime()) / (1000 * 60 * 60 * 24));

    if (diffDays < 0) {
      return <Badge variant="destructive">Atrasado</Badge>;
    } else if (diffDays <= 7) {
      return <Badge className="bg-yellow-500 hover:bg-yellow-600">Urgente</Badge>;
    } else {
      return <Badge className="bg-green-500 hover:bg-green-600">No prazo</Badge>;
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900">
      <Navbar />
      <div className="container mx-auto px-4 py-8">
        <div className="flex justify-between items-center mb-8">
          <div>
            <h1 className="text-3xl font-bold text-gray-900 dark:text-white">
              Meus Projetos
            </h1>
            <p className="text-gray-600 dark:text-gray-400 mt-2">
              Gerencie seus projetos e acompanhe os prazos
            </p>
          </div>
          
          <Dialog open={dialogOpen} onOpenChange={setDialogOpen}>
            <DialogTrigger asChild>
              <Button className="flex items-center space-x-2">
                <Plus className="h-4 w-4" />
                <span>Novo Projeto</span>
              </Button>
            </DialogTrigger>
            <DialogContent>
              <DialogHeader>
                <DialogTitle>Criar Novo Projeto</DialogTitle>
                <DialogDescription>
                  Preencha as informações do projeto abaixo
                </DialogDescription>
              </DialogHeader>
              <form onSubmit={handleSubmit} className="space-y-4">
                <div className="space-y-2">
                  <Label htmlFor="nome">Nome do Projeto</Label>
                  <Input
                    id="nome"
                    type="text"
                    placeholder="Ex: Website Corporativo"
                    value={nome}
                    onChange={(e) => setNome(e.target.value)}
                    required
                  />
                </div>
                <div className="space-y-2">
                  <Label htmlFor="dataSolicitacao">Data de Solicitação</Label>
                  <Input
                    id="dataSolicitacao"
                    type="date"
                    value={dataSolicitacao}
                    onChange={(e) => setDataSolicitacao(e.target.value)}
                    required
                  />
                </div>
                <div className="space-y-2">
                  <Label htmlFor="prazoEntrega">Prazo de Entrega</Label>
                  <Input
                    id="prazoEntrega"
                    type="date"
                    value={prazoEntrega}
                    onChange={(e) => setPrazoEntrega(e.target.value)}
                    required
                  />
                </div>
                <div className="flex justify-end space-x-2">
                  <Button 
                    type="button" 
                    variant="outline"
                    onClick={() => setDialogOpen(false)}
                  >
                    Cancelar
                  </Button>
                  <Button type="submit" disabled={isLoading}>
                    {isLoading ? 'Criando...' : 'Criar Projeto'}
                  </Button>
                </div>
              </form>
            </DialogContent>
          </Dialog>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {projetos.map((projeto) => (
            <Card key={projeto.id} className="hover:shadow-lg transition-shadow animate-fade-in">
              <CardHeader>
                <div className="flex justify-between items-start">
                  <CardTitle className="text-lg">{projeto.nome}</CardTitle>
                  {getStatusBadge(projeto.prazo_entrega)}
                </div>
              </CardHeader>
              <CardContent>
                <div className="space-y-3">
                  <div className="flex items-center text-sm text-gray-600 dark:text-gray-400">
                    <Calendar className="h-4 w-4 mr-2" />
                    Solicitado: {new Date(projeto.data_solicitacao).toLocaleDateString()}
                  </div>
                  <div className="flex items-center text-sm text-gray-600 dark:text-gray-400">
                    <Clock className="h-4 w-4 mr-2" />
                    Prazo: {new Date(projeto.prazo_entrega).toLocaleDateString()}
                  </div>
                  <div className="flex items-center text-sm text-gray-600 dark:text-gray-400">
                    <User className="h-4 w-4 mr-2" />
                    {user?.nome}
                  </div>
                </div>
              </CardContent>
            </Card>
          ))}
        </div>

        {projetos.length === 0 && (
          <div className="text-center py-12">
            <div className="mx-auto h-24 w-24 bg-gray-100 dark:bg-gray-800 rounded-full flex items-center justify-center mb-4">
              <Plus className="h-12 w-12 text-gray-400" />
            </div>
            <h3 className="text-lg font-medium text-gray-900 dark:text-gray-100 mb-2">
              Nenhum projeto encontrado
            </h3>
            <p className="text-gray-500 dark:text-gray-400 mb-4">
              Comece criando seu primeiro projeto
            </p>
            <Button onClick={() => setDialogOpen(true)}>
              <Plus className="h-4 w-4 mr-2" />
              Criar Primeiro Projeto
            </Button>
          </div>
        )}
      </div>
    </div>
  );
};

export default Projetos;
