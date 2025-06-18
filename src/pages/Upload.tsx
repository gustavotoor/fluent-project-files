
import { useState, useEffect } from 'react';
import { useAuth } from '@/contexts/AuthContext';
import { Button } from '@/components/ui/button';
import { Label } from '@/components/ui/label';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import Navbar from '@/components/Navbar';
import { Upload as UploadIcon, FileText, Image, FileSpreadsheet, File } from 'lucide-react';
import { useToast } from '@/hooks/use-toast';

interface Projeto {
  id: string;
  nome: string;
}

interface ArquivoUpload {
  id: string;
  nome_arquivo: string;
  tipo: string;
  projeto_id: string;
  data_upload: string;
}

const Upload = () => {
  const [projetos, setProjetos] = useState<Projeto[]>([]);
  const [selectedProjeto, setSelectedProjeto] = useState<string>('');
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [uploads, setUploads] = useState<ArquivoUpload[]>([]);
  const { user } = useAuth();
  const { toast } = useToast();

  const allowedTypes = [
    'application/pdf',
    'application/msword',
    'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
    'application/vnd.ms-excel',
    'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    'image/jpeg',
    'image/jpg',
    'text/plain'
  ];

  useEffect(() => {
    loadProjetos();
    loadUploads();
  }, []);

  const loadProjetos = async () => {
    try {
      // Simulate API call to get distinct projects
      const demoProjetos: Projeto[] = [
        { id: '1', nome: 'Website Corporativo' },
        { id: '2', nome: 'Sistema de Vendas' },
        { id: '3', nome: 'App Mobile' }
      ];
      setProjetos(demoProjetos);
    } catch (error) {
      console.error('Error loading projects:', error);
    }
  };

  const loadUploads = async () => {
    try {
      // Simulate API call to get user uploads
      const demoUploads: ArquivoUpload[] = [
        {
          id: '1',
          nome_arquivo: 'proposta.pdf',
          tipo: 'application/pdf',
          projeto_id: '1',
          data_upload: new Date().toISOString()
        },
        {
          id: '2',
          nome_arquivo: 'layout.jpg',
          tipo: 'image/jpeg',
          projeto_id: '1',
          data_upload: new Date(Date.now() - 86400000).toISOString()
        }
      ];
      setUploads(demoUploads);
    } catch (error) {
      console.error('Error loading uploads:', error);
    }
  };

  const handleFileSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      if (allowedTypes.includes(file.type)) {
        setSelectedFile(file);
      } else {
        toast({
          title: "Tipo de arquivo não permitido",
          description: "Por favor, selecione um arquivo PDF, DOC, DOCX, XLS, XLSX, JPG, JPEG ou TXT",
          variant: "destructive",
        });
        e.target.value = '';
      }
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!selectedFile || !selectedProjeto) {
      toast({
        title: "Campos obrigatórios",
        description: "Selecione um arquivo e um projeto",
        variant: "destructive",
      });
      return;
    }

    setIsLoading(true);

    try {
      // Simulate file upload
      const novoUpload: ArquivoUpload = {
        id: Date.now().toString(),
        nome_arquivo: selectedFile.name,
        tipo: selectedFile.type,
        projeto_id: selectedProjeto,
        data_upload: new Date().toISOString()
      };

      setUploads(prev => [novoUpload, ...prev]);
      
      // Clear form
      setSelectedFile(null);
      setSelectedProjeto('');
      const fileInput = document.getElementById('file-upload') as HTMLInputElement;
      if (fileInput) fileInput.value = '';
      
      toast({
        title: "Upload realizado com sucesso!",
        description: `O arquivo "${selectedFile.name}" foi enviado.`,
      });
    } catch (error) {
      toast({
        title: "Erro no upload",
        description: "Não foi possível enviar o arquivo",
        variant: "destructive",
      });
    } finally {
      setIsLoading(false);
    }
  };

  const getFileIcon = (type: string) => {
    if (type.includes('pdf')) return <FileText className="h-5 w-5 text-red-500" />;
    if (type.includes('image')) return <Image className="h-5 w-5 text-green-500" />;
    if (type.includes('sheet') || type.includes('excel')) return <FileSpreadsheet className="h-5 w-5 text-blue-500" />;
    return <File className="h-5 w-5 text-gray-500" />;
  };

  const getProjetoNome = (projetoId: string) => {
    const projeto = projetos.find(p => p.id === projetoId);
    return projeto?.nome || 'Projeto não encontrado';
  };

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900">
      <Navbar />
      <div className="container mx-auto px-4 py-8">
        <div className="max-w-4xl mx-auto">
          <h1 className="text-3xl font-bold text-gray-900 dark:text-white mb-2">
            Upload de Arquivos
          </h1>
          <p className="text-gray-600 dark:text-gray-400 mb-8">
            Envie arquivos vinculados aos seus projetos
          </p>

          <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
            {/* Upload Form */}
            <Card>
              <CardHeader>
                <CardTitle>Enviar Arquivo</CardTitle>
                <CardDescription>
                  Selecione um arquivo e o projeto relacionado
                </CardDescription>
              </CardHeader>
              <CardContent>
                <form onSubmit={handleSubmit} className="space-y-6">
                  <div className="space-y-2">
                    <Label htmlFor="projeto">Projeto</Label>
                    <Select value={selectedProjeto} onValueChange={setSelectedProjeto}>
                      <SelectTrigger>
                        <SelectValue placeholder="Selecione um projeto" />
                      </SelectTrigger>
                      <SelectContent>
                        {projetos.map((projeto) => (
                          <SelectItem key={projeto.id} value={projeto.id}>
                            {projeto.nome}
                          </SelectItem>
                        ))}
                      </SelectContent>
                    </Select>
                  </div>

                  <div className="space-y-2">
                    <Label htmlFor="file-upload">Arquivo</Label>
                    <div className="border-2 border-dashed border-gray-300 dark:border-gray-600 rounded-lg p-6 text-center hover:border-primary transition-colors">
                      <UploadIcon className="mx-auto h-12 w-12 text-gray-400 mb-4" />
                      <div className="text-sm text-gray-600 dark:text-gray-400 mb-2">
                        <label htmlFor="file-upload" className="cursor-pointer text-primary hover:text-primary/80">
                          Clique para selecionar
                        </label>
                        <span> ou arraste um arquivo</span>
                      </div>
                      <p className="text-xs text-gray-500">
                        PDF, DOC, DOCX, XLS, XLSX, JPG, JPEG, TXT (máx. 10MB)
                      </p>
                      <input
                        id="file-upload"
                        type="file"
                        className="hidden"
                        onChange={handleFileSelect}
                        accept=".pdf,.doc,.docx,.xls,.xlsx,.jpg,.jpeg,.txt"
                      />
                    </div>
                    {selectedFile && (
                      <div className="flex items-center space-x-2 text-sm text-gray-600 dark:text-gray-400">
                        {getFileIcon(selectedFile.type)}
                        <span>{selectedFile.name}</span>
                        <span>({(selectedFile.size / 1024 / 1024).toFixed(2)} MB)</span>
                      </div>
                    )}
                  </div>

                  <Button 
                    type="submit" 
                    disabled={!selectedFile || !selectedProjeto || isLoading}
                    className="w-full"
                  >
                    {isLoading ? 'Enviando...' : 'Enviar Arquivo'}
                  </Button>
                </form>
              </CardContent>
            </Card>

            {/* Recent Uploads */}
            <Card>
              <CardHeader>
                <CardTitle>Uploads Recentes</CardTitle>
                <CardDescription>
                  Seus arquivos enviados recentemente
                </CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-4 max-h-96 overflow-y-auto">
                  {uploads.map((upload) => (
                    <div key={upload.id} className="flex items-center space-x-3 p-3 border rounded-lg hover:bg-gray-50 dark:hover:bg-gray-800 transition-colors">
                      {getFileIcon(upload.tipo)}
                      <div className="flex-1 min-w-0">
                        <p className="text-sm font-medium text-gray-900 dark:text-gray-100 truncate">
                          {upload.nome_arquivo}
                        </p>
                        <p className="text-xs text-gray-500 dark:text-gray-400">
                          {getProjetoNome(upload.projeto_id)}
                        </p>
                        <p className="text-xs text-gray-400">
                          {new Date(upload.data_upload).toLocaleDateString()} às{' '}
                          {new Date(upload.data_upload).toLocaleTimeString()}
                        </p>
                      </div>
                    </div>
                  ))}
                </div>

                {uploads.length === 0 && (
                  <div className="text-center py-8">
                    <UploadIcon className="mx-auto h-12 w-12 text-gray-400 mb-4" />
                    <p className="text-gray-500 dark:text-gray-400">
                      Nenhum arquivo enviado ainda
                    </p>
                  </div>
                )}
              </CardContent>
            </Card>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Upload;
